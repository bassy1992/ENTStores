from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product, Category
from shop.cloud_storage import PermanentStorage
import os
import requests
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Migrate media files to permanent cloud storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--setup-github',
            action='store_true',
            help='Set up GitHub repository for media storage',
        )
        parser.add_argument(
            '--migrate-all',
            action='store_true',
            help='Migrate all media files to permanent storage',
        )
        parser.add_argument(
            '--create-placeholders',
            action='store_true',
            help='Create placeholder files and upload to permanent storage',
        )
        parser.add_argument(
            '--verify',
            action='store_true',
            help='Verify all files are accessible',
        )

    def handle(self, *args, **options):
        if options['setup_github']:
            self.setup_github_repo()
        elif options['migrate_all']:
            self.migrate_all_files()
        elif options['create_placeholders']:
            self.create_and_upload_placeholders()
        elif options['verify']:
            self.verify_all_files()
        else:
            self.show_status()

    def setup_github_repo(self):
        """Instructions for setting up GitHub repository"""
        self.stdout.write("🔧 GitHub Repository Setup Instructions:")
        self.stdout.write("=" * 50)
        self.stdout.write("1. Go to https://github.com/new")
        self.stdout.write("2. Create repository: 'ENTstore-media'")
        self.stdout.write("3. Make it PUBLIC (for free CDN access)")
        self.stdout.write("4. Create a Personal Access Token:")
        self.stdout.write("   - Go to GitHub Settings > Developer settings > Personal access tokens")
        self.stdout.write("   - Generate new token with 'repo' permissions")
        self.stdout.write("5. Add token to Render environment variables:")
        self.stdout.write("   - GITHUB_TOKEN=your_token_here")
        self.stdout.write("")
        self.stdout.write("✅ After setup, run: python manage.py migrate_to_permanent --migrate-all")

    def create_and_upload_placeholders(self):
        """Create placeholder images and upload to permanent storage"""
        self.stdout.write("🖼️ Creating and uploading placeholder images...")
        
        storage = PermanentStorage()
        
        # Create placeholder image data
        placeholder_data = self.create_placeholder_image_data()
        
        created_count = 0
        
        # Handle products
        for product in Product.objects.exclude(image=''):
            if product.image:
                file_name = str(product.image)
                
                try:
                    # Create placeholder file
                    placeholder_file = ContentFile(placeholder_data, name=file_name)
                    
                    # Save to permanent storage
                    saved_name = storage._save(file_name, placeholder_file)
                    
                    # Update product image field to point to saved file
                    product.image.name = saved_name
                    product.save(update_fields=['image'])
                    
                    self.stdout.write(f"✅ Created placeholder for product: {file_name}")
                    created_count += 1
                    
                except Exception as e:
                    self.stdout.write(f"❌ Failed to create placeholder for {file_name}: {e}")
        
        # Handle categories
        for category in Category.objects.exclude(image=''):
            if category.image:
                file_name = str(category.image)
                
                try:
                    # Create placeholder file
                    placeholder_file = ContentFile(placeholder_data, name=file_name)
                    
                    # Save to permanent storage
                    saved_name = storage._save(file_name, placeholder_file)
                    
                    # Update category image field
                    category.image.name = saved_name
                    category.save(update_fields=['image'])
                    
                    self.stdout.write(f"✅ Created placeholder for category: {file_name}")
                    created_count += 1
                    
                except Exception as e:
                    self.stdout.write(f"❌ Failed to create placeholder for {file_name}: {e}")
        
        self.stdout.write(f"🎉 Created {created_count} placeholder images in permanent storage!")

    def create_placeholder_image_data(self):
        """Create minimal JPEG image data"""
        # Minimal valid JPEG file (1x1 pixel gray image)
        return (
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
            b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08'
            b'\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e'
            b'\x1d\x1a\x1c\x1c $.\' \",#\x1c\x1c(7),01444\x1f\'9=82<.342'
            b'\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01'
            b'\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        )

    def migrate_all_files(self):
        """Migrate existing files to permanent storage"""
        self.stdout.write("🚀 Migrating all files to permanent storage...")
        
        storage = PermanentStorage()
        migrated_count = 0
        
        # Migrate product images
        for product in Product.objects.exclude(image=''):
            if product.image:
                try:
                    # Check if file exists locally
                    local_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
                    
                    if os.path.exists(local_path):
                        # Read local file
                        with open(local_path, 'rb') as f:
                            file_content = ContentFile(f.read(), name=str(product.image))
                        
                        # Save to permanent storage
                        saved_name = storage._save(str(product.image), file_content)
                        
                        self.stdout.write(f"✅ Migrated product image: {product.image}")
                        migrated_count += 1
                    else:
                        self.stdout.write(f"⚠️  Local file not found: {product.image}")
                        
                except Exception as e:
                    self.stdout.write(f"❌ Failed to migrate {product.image}: {e}")
        
        # Migrate category images
        for category in Category.objects.exclude(image=''):
            if category.image:
                try:
                    local_path = os.path.join(settings.MEDIA_ROOT, str(category.image))
                    
                    if os.path.exists(local_path):
                        with open(local_path, 'rb') as f:
                            file_content = ContentFile(f.read(), name=str(category.image))
                        
                        saved_name = storage._save(str(category.image), file_content)
                        
                        self.stdout.write(f"✅ Migrated category image: {category.image}")
                        migrated_count += 1
                    else:
                        self.stdout.write(f"⚠️  Local file not found: {category.image}")
                        
                except Exception as e:
                    self.stdout.write(f"❌ Failed to migrate {category.image}: {e}")
        
        if migrated_count == 0:
            self.stdout.write("ℹ️  No local files found to migrate. Creating placeholders...")
            self.create_and_upload_placeholders()
        else:
            self.stdout.write(f"🎉 Migrated {migrated_count} files to permanent storage!")

    def verify_all_files(self):
        """Verify all files are accessible via permanent storage"""
        self.stdout.write("🔍 Verifying all files in permanent storage...")
        
        storage = PermanentStorage()
        verified_count = 0
        missing_count = 0
        
        # Verify product images
        for product in Product.objects.exclude(image=''):
            if product.image:
                try:
                    if storage.exists(str(product.image)):
                        url = storage.url(str(product.image))
                        self.stdout.write(f"✅ Product {product.id}: {url}")
                        verified_count += 1
                    else:
                        self.stdout.write(f"❌ Missing: {product.image}")
                        missing_count += 1
                except Exception as e:
                    self.stdout.write(f"❌ Error checking {product.image}: {e}")
                    missing_count += 1
        
        # Verify category images
        for category in Category.objects.exclude(image=''):
            if category.image:
                try:
                    if storage.exists(str(category.image)):
                        url = storage.url(str(category.image))
                        self.stdout.write(f"✅ Category {category.key}: {url}")
                        verified_count += 1
                    else:
                        self.stdout.write(f"❌ Missing: {category.image}")
                        missing_count += 1
                except Exception as e:
                    self.stdout.write(f"❌ Error checking {category.image}: {e}")
                    missing_count += 1
        
        self.stdout.write(f"📊 Verification complete: {verified_count} verified, {missing_count} missing")
        
        if missing_count > 0:
            self.stdout.write("💡 Run --create-placeholders to fix missing files")

    def show_status(self):
        """Show current permanent storage status"""
        self.stdout.write("🛡️ Permanent Storage Status")
        self.stdout.write("=" * 40)
        
        # Check configuration
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            self.stdout.write(f"✅ GitHub token configured (length: {len(github_token)})")
        else:
            self.stdout.write("❌ GitHub token not configured")
        
        # Check storage
        storage = PermanentStorage()
        self.stdout.write(f"📦 Storage backends: {len(storage.backends)}")
        
        for backend in storage.backends:
            self.stdout.write(f"   - {backend.__class__.__name__}")
        
        # Check database
        products_with_images = Product.objects.exclude(image='').count()
        categories_with_images = Category.objects.exclude(image='').count()
        
        self.stdout.write(f"🛍️  Products with images: {products_with_images}")
        self.stdout.write(f"🏷️  Categories with images: {categories_with_images}")
        
        self.stdout.write("\n💡 Next steps:")
        if not github_token:
            self.stdout.write("1. Run --setup-github to get setup instructions")
        else:
            self.stdout.write("1. Run --create-placeholders to create permanent files")
            self.stdout.write("2. Run --verify to check all files are accessible")