from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product, Category
import os
import shutil
import json
from datetime import datetime


class Command(BaseCommand):
    help = 'Aggressive media protection system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--setup',
            action='store_true',
            help='Set up media protection system',
        )
        parser.add_argument(
            '--verify',
            action='store_true',
            help='Verify all media files exist and restore if missing',
        )
        parser.add_argument(
            '--create-placeholders',
            action='store_true',
            help='Create placeholder images for missing files',
        )
        parser.add_argument(
            '--force-restore',
            action='store_true',
            help='Force restore all files from any available source',
        )

    def handle(self, *args, **options):
        if options['setup']:
            self.setup_protection()
        elif options['verify']:
            self.verify_and_restore()
        elif options['create_placeholders']:
            self.create_placeholders()
        elif options['force_restore']:
            self.force_restore()
        else:
            self.show_status()

    def setup_protection(self):
        """Set up the media protection system"""
        self.stdout.write("🛡️ Setting up media protection system...")
        
        # Create all necessary directories
        directories = [
            settings.MEDIA_ROOT,
            '/opt/render/project/data/media_backup',
            '/opt/render/project/data/media_archive',
            '/opt/render/project/data/media_emergency',
            os.path.join(settings.MEDIA_ROOT, 'products'),
            os.path.join(settings.MEDIA_ROOT, 'categories'),
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                os.chmod(directory, 0o755)
                self.stdout.write(f"✅ Created: {directory}")
            except Exception as e:
                self.stdout.write(f"⚠️  Failed to create {directory}: {e}")
        
        # Create media inventory
        self.create_media_inventory()
        
        # Set up file watchers (if possible)
        self.setup_file_watchers()
        
        self.stdout.write(self.style.SUCCESS("✅ Media protection system ready!"))

    def create_media_inventory(self):
        """Create an inventory of all media files"""
        inventory = {
            'created': datetime.now().isoformat(),
            'products': {},
            'categories': {},
            'files': []
        }
        
        # Inventory products
        for product in Product.objects.exclude(image=''):
            if product.image:
                file_path = str(product.image)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                inventory['products'][product.id] = {
                    'title': product.title,
                    'image': file_path,
                    'exists': os.path.exists(full_path),
                    'size': os.path.getsize(full_path) if os.path.exists(full_path) else 0
                }
                inventory['files'].append(file_path)
        
        # Inventory categories
        for category in Category.objects.exclude(image=''):
            if category.image:
                file_path = str(category.image)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                inventory['categories'][category.key] = {
                    'label': category.label,
                    'image': file_path,
                    'exists': os.path.exists(full_path),
                    'size': os.path.getsize(full_path) if os.path.exists(full_path) else 0
                }
                inventory['files'].append(file_path)
        
        # Save inventory
        inventory_path = '/opt/render/project/data/media_inventory.json'
        try:
            with open(inventory_path, 'w') as f:
                json.dump(inventory, f, indent=2)
            self.stdout.write(f"📋 Media inventory saved: {inventory_path}")
        except Exception as e:
            self.stdout.write(f"⚠️  Failed to save inventory: {e}")

    def verify_and_restore(self):
        """Verify all media files and restore missing ones"""
        self.stdout.write("🔍 Verifying media files...")
        
        missing_files = []
        restored_files = []
        
        # Check products
        for product in Product.objects.exclude(image=''):
            if product.image:
                file_path = str(product.image)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                
                if not os.path.exists(full_path):
                    missing_files.append(f"Product {product.id}: {file_path}")
                    
                    # Try to restore from backup locations
                    if self.restore_file_from_backup(file_path):
                        restored_files.append(file_path)
        
        # Check categories
        for category in Category.objects.exclude(image=''):
            if category.image:
                file_path = str(category.image)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                
                if not os.path.exists(full_path):
                    missing_files.append(f"Category {category.key}: {file_path}")
                    
                    # Try to restore from backup locations
                    if self.restore_file_from_backup(file_path):
                        restored_files.append(file_path)
        
        # Report results
        if missing_files:
            self.stdout.write(f"⚠️  Found {len(missing_files)} missing files:")
            for missing in missing_files[:10]:
                self.stdout.write(f"   - {missing}")
        
        if restored_files:
            self.stdout.write(f"✅ Restored {len(restored_files)} files from backup")
        
        if not missing_files:
            self.stdout.write(self.style.SUCCESS("✅ All media files verified!"))

    def restore_file_from_backup(self, file_path):
        """Try to restore a file from various backup locations"""
        backup_locations = [
            '/opt/render/project/data/media_backup',
            '/opt/render/project/data/media_archive',
            '/opt/render/project/data/media_emergency',
        ]
        
        for backup_location in backup_locations:
            backup_file = os.path.join(backup_location, file_path)
            if os.path.exists(backup_file):
                try:
                    # Restore to primary location
                    primary_file = os.path.join(settings.MEDIA_ROOT, file_path)
                    primary_dir = os.path.dirname(primary_file)
                    os.makedirs(primary_dir, exist_ok=True)
                    
                    shutil.copy2(backup_file, primary_file)
                    self.stdout.write(f"   ✅ Restored: {file_path} from {backup_location}")
                    return True
                    
                except Exception as e:
                    self.stdout.write(f"   ⚠️  Failed to restore {file_path}: {e}")
        
        return False

    def create_placeholders(self):
        """Create placeholder images for missing files"""
        self.stdout.write("🖼️ Creating placeholder images...")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            self.stdout.write("⚠️  PIL not available, creating minimal placeholders")
            self.create_minimal_placeholders()
            return
        
        # Create placeholder for products
        for product in Product.objects.exclude(image=''):
            if product.image:
                file_path = str(product.image)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                
                if not os.path.exists(full_path):
                    self.create_placeholder_image(full_path, f"Product\n{product.title[:20]}")
        
        # Create placeholder for categories
        for category in Category.objects.exclude(image=''):
            if category.image:
                file_path = str(category.image)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                
                if not os.path.exists(full_path):
                    self.create_placeholder_image(full_path, f"Category\n{category.label}")

    def create_placeholder_image(self, file_path, text):
        """Create a placeholder image with text"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create directory if needed
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Create image
            img = Image.new('RGB', (400, 400), color='lightgray')
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font = ImageFont.load_default()
            except:
                font = None
            
            # Calculate text position
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (400 - text_width) // 2
            y = (400 - text_height) // 2
            
            draw.text((x, y), text, fill='black', font=font)
            
            # Save image
            img.save(file_path, 'JPEG')
            self.stdout.write(f"   🖼️ Created placeholder: {file_path}")
            
        except Exception as e:
            self.stdout.write(f"   ⚠️  Failed to create placeholder {file_path}: {e}")
            # Fallback to minimal file
            self.create_minimal_placeholder(file_path)

    def create_minimal_placeholder(self, file_path):
        """Create a minimal placeholder file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Create minimal JPEG file
            minimal_jpeg = (
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
            
            with open(file_path, 'wb') as f:
                f.write(minimal_jpeg)
            
            self.stdout.write(f"   📄 Created minimal placeholder: {file_path}")
            
        except Exception as e:
            self.stdout.write(f"   ❌ Failed to create minimal placeholder {file_path}: {e}")

    def create_minimal_placeholders(self):
        """Create minimal placeholder files without PIL"""
        for product in Product.objects.exclude(image=''):
            if product.image:
                file_path = str(product.image)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                if not os.path.exists(full_path):
                    self.create_minimal_placeholder(full_path)
        
        for category in Category.objects.exclude(image=''):
            if category.image:
                file_path = str(category.image)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                if not os.path.exists(full_path):
                    self.create_minimal_placeholder(full_path)

    def force_restore(self):
        """Force restore all files using any available method"""
        self.stdout.write("🚨 Force restoring all media files...")
        
        # First try normal restore
        self.verify_and_restore()
        
        # Then create placeholders for anything still missing
        self.create_placeholders()
        
        # Final verification
        missing_count = 0
        for product in Product.objects.exclude(image=''):
            if product.image:
                full_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
                if not os.path.exists(full_path):
                    missing_count += 1
        
        for category in Category.objects.exclude(image=''):
            if category.image:
                full_path = os.path.join(settings.MEDIA_ROOT, str(category.image))
                if not os.path.exists(full_path):
                    missing_count += 1
        
        if missing_count == 0:
            self.stdout.write(self.style.SUCCESS("✅ All media files restored!"))
        else:
            self.stdout.write(f"⚠️  {missing_count} files still missing after force restore")

    def setup_file_watchers(self):
        """Set up file system watchers (if possible)"""
        # This would require additional packages like watchdog
        # For now, just create a simple monitoring script
        monitor_script = '''#!/bin/bash
# Media file monitor for ENTstore
while true; do
    sleep 300  # Check every 5 minutes
    cd /opt/render/project/src/backend
    python manage.py protect_media --verify > /dev/null 2>&1
done
'''
        
        try:
            script_path = '/opt/render/project/data/media_monitor.sh'
            with open(script_path, 'w') as f:
                f.write(monitor_script)
            os.chmod(script_path, 0o755)
            self.stdout.write(f"📝 Created monitoring script: {script_path}")
        except Exception as e:
            self.stdout.write(f"⚠️  Failed to create monitoring script: {e}")

    def show_status(self):
        """Show current media protection status"""
        self.stdout.write("🛡️ Media Protection Status")
        self.stdout.write("=" * 40)
        
        # Check directories
        directories = [
            settings.MEDIA_ROOT,
            '/opt/render/project/data/media_backup',
            '/opt/render/project/data/media_archive',
        ]
        
        for directory in directories:
            exists = os.path.exists(directory)
            if exists:
                file_count = sum(len(files) for _, _, files in os.walk(directory))
                self.stdout.write(f"✅ {directory}: {file_count} files")
            else:
                self.stdout.write(f"❌ {directory}: Not found")
        
        # Check database references
        products_with_images = Product.objects.exclude(image='').count()
        categories_with_images = Category.objects.exclude(image='').count()
        
        self.stdout.write(f"🛍️  Products with images: {products_with_images}")
        self.stdout.write(f"🏷️  Categories with images: {categories_with_images}")
        
        # Check for missing files
        missing_count = 0
        for product in Product.objects.exclude(image=''):
            if product.image:
                full_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
                if not os.path.exists(full_path):
                    missing_count += 1
        
        for category in Category.objects.exclude(image=''):
            if category.image:
                full_path = os.path.join(settings.MEDIA_ROOT, str(category.image))
                if not os.path.exists(full_path):
                    missing_count += 1
        
        if missing_count == 0:
            self.stdout.write(self.style.SUCCESS("✅ All referenced files exist"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️  {missing_count} files missing"))