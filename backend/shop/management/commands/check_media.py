from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product, Category
import os


class Command(BaseCommand):
    help = 'Check media files configuration and status'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix-missing',
            action='store_true',
            help='Try to fix missing media files by creating placeholders',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Checking media files configuration...'))
        
        # Check media root
        self.stdout.write(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
        self.stdout.write(f"🌐 MEDIA_URL: {settings.MEDIA_URL}")
        
        # Check if media root exists
        if os.path.exists(settings.MEDIA_ROOT):
            self.stdout.write(self.style.SUCCESS(f"✅ Media root exists"))
            
            # List subdirectories
            subdirs = [d for d in os.listdir(settings.MEDIA_ROOT) 
                      if os.path.isdir(os.path.join(settings.MEDIA_ROOT, d))]
            self.stdout.write(f"📂 Subdirectories: {subdirs}")
            
            # Count files
            total_files = 0
            for root, dirs, files in os.walk(settings.MEDIA_ROOT):
                total_files += len(files)
            self.stdout.write(f"📄 Total media files: {total_files}")
            
        else:
            self.stdout.write(self.style.ERROR(f"❌ Media root does not exist"))
            if options['fix_missing']:
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'products'), exist_ok=True)
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'categories'), exist_ok=True)
                self.stdout.write(self.style.SUCCESS(f"✅ Created media directories"))
        
        # Check products with images
        products_with_images = Product.objects.exclude(image='').count()
        products_total = Product.objects.count()
        self.stdout.write(f"🛍️  Products with images: {products_with_images}/{products_total}")
        
        # Check categories with images
        categories_with_images = Category.objects.exclude(image='').count()
        categories_total = Category.objects.count()
        self.stdout.write(f"🏷️  Categories with images: {categories_with_images}/{categories_total}")
        
        # Check for missing files
        missing_files = []
        
        for product in Product.objects.exclude(image=''):
            if product.image:
                full_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
                if not os.path.exists(full_path):
                    missing_files.append(f"Product {product.id}: {product.image}")
        
        for category in Category.objects.exclude(image=''):
            if category.image:
                full_path = os.path.join(settings.MEDIA_ROOT, str(category.image))
                if not os.path.exists(full_path):
                    missing_files.append(f"Category {category.key}: {category.image}")
        
        if missing_files:
            self.stdout.write(self.style.WARNING(f"⚠️  Missing files ({len(missing_files)}):"))
            for missing in missing_files[:10]:  # Show first 10
                self.stdout.write(f"   - {missing}")
            if len(missing_files) > 10:
                self.stdout.write(f"   ... and {len(missing_files) - 10} more")
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ All referenced media files exist"))
        
        # Environment info
        self.stdout.write(f"\n🔧 Environment:")
        self.stdout.write(f"   DEBUG: {settings.DEBUG}")
        self.stdout.write(f"   RENDER: {os.getenv('RENDER', 'False')}")
        
        # Disk usage (if on Render)
        if os.path.exists('/opt/render/project/data'):
            try:
                import shutil
                total, used, free = shutil.disk_usage('/opt/render/project/data')
                self.stdout.write(f"💾 Persistent disk usage:")
                self.stdout.write(f"   Total: {total // (1024**3):.1f} GB")
                self.stdout.write(f"   Used: {used // (1024**3):.1f} GB")
                self.stdout.write(f"   Free: {free // (1024**3):.1f} GB")
            except:
                pass
        
        self.stdout.write(self.style.SUCCESS('\n✅ Media check completed!'))