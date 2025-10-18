"""
Django management command to restore media URLs
This runs automatically after Railway deployments
"""
import os
import json
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product, Category, ProductImage


class Command(BaseCommand):
    help = 'Restore media URLs from environment variables or backup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from-env',
            action='store_true',
            help='Restore from environment variables',
        )
        parser.add_argument(
            '--from-backup',
            type=str,
            help='Restore from backup file',
        )
        parser.add_argument(
            '--auto',
            action='store_true',
            help='Auto-detect and restore from best available source',
        )

    def handle(self, *args, **options):
        self.stdout.write("🔄 Starting media URL restoration...")
        
        if options['auto']:
            # Try environment variables first, then backup files
            if self.restore_from_environment():
                return
            elif self.restore_from_backup_files():
                return
            else:
                self.stdout.write(self.style.ERROR("❌ No restoration source found"))
        elif options['from_env']:
            self.restore_from_environment()
        elif options['from_backup']:
            self.restore_from_backup_file(options['from_backup'])
        else:
            # Default: auto mode
            if self.restore_from_environment():
                return
            elif self.restore_from_backup_files():
                return
            else:
                self.stdout.write(self.style.ERROR("❌ No restoration source found"))

    def restore_from_environment(self):
        """Restore URLs from environment variables"""
        self.stdout.write("🔍 Checking environment variables...")
        
        restored_count = 0
        env_vars_found = 0
        
        # Restore product URLs
        for key, value in os.environ.items():
            if key.startswith('PRODUCT_IMG_'):
                env_vars_found += 1
                product_id = key.replace('PRODUCT_IMG_', '')
                try:
                    product = Product.objects.get(id=product_id)
                    if not product.image_url or product.image_url != value:
                        product.image_url = value
                        product.save(update_fields=['image_url'])
                        restored_count += 1
                        self.stdout.write(f"✅ Restored product: {product.title}")
                except Product.DoesNotExist:
                    self.stdout.write(f"⚠️  Product not found: {product_id}")
            
            elif key.startswith('CATEGORY_IMG_'):
                env_vars_found += 1
                category_key = key.replace('CATEGORY_IMG_', '')
                try:
                    category = Category.objects.get(key=category_key)
                    if not category.image_url or category.image_url != value:
                        category.image_url = value
                        category.save(update_fields=['image_url'])
                        restored_count += 1
                        self.stdout.write(f"✅ Restored category: {category.label}")
                except Category.DoesNotExist:
                    self.stdout.write(f"⚠️  Category not found: {category_key}")
            
            elif key.startswith('PRODIMG_'):
                env_vars_found += 1
                img_id = key.replace('PRODIMG_', '')
                try:
                    img = ProductImage.objects.get(id=img_id)
                    if not img.image_url or img.image_url != value:
                        img.image_url = value
                        img.save(update_fields=['image_url'])
                        restored_count += 1
                        self.stdout.write(f"✅ Restored product image: {img.product.title}")
                except ProductImage.DoesNotExist:
                    self.stdout.write(f"⚠️  Product image not found: {img_id}")
        
        if env_vars_found > 0:
            self.stdout.write(
                self.style.SUCCESS(f"✅ Restored {restored_count}/{env_vars_found} URLs from environment variables")
            )
            return True
        else:
            self.stdout.write("ℹ️  No media URL environment variables found")
            return False

    def restore_from_backup_files(self):
        """Find and restore from the latest backup file"""
        import glob
        
        # Look for backup files in multiple locations
        backup_patterns = [
            'media_urls_backup_*.json',
            '../media_urls_backup_*.json',
            '/app/media_urls_backup_*.json',
            '/tmp/media_urls_backup_*.json'
        ]
        
        backup_files = []
        for pattern in backup_patterns:
            backup_files.extend(glob.glob(pattern))
        
        if not backup_files:
            self.stdout.write("ℹ️  No backup files found")
            return False
        
        # Use the latest backup
        latest_backup = max(backup_files, key=os.path.getctime)
        self.stdout.write(f"📁 Found backup: {latest_backup}")
        
        return self.restore_from_backup_file(latest_backup)

    def restore_from_backup_file(self, backup_file):
        """Restore from a specific backup file"""
        if not os.path.exists(backup_file):
            self.stdout.write(self.style.ERROR(f"❌ Backup file not found: {backup_file}"))
            return False
        
        self.stdout.write(f"🔄 Restoring from: {backup_file}")
        
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to read backup file: {e}"))
            return False
        
        restored_count = 0
        
        # Restore product URLs
        for product_data in backup_data.get('products', []):
            try:
                product = Product.objects.get(id=product_data['id'])
                if not product.image_url:  # Only restore if empty
                    product.image_url = product_data['image_url']
                    product.save(update_fields=['image_url'])
                    restored_count += 1
                    self.stdout.write(f"✅ Restored product: {product.title}")
            except Product.DoesNotExist:
                self.stdout.write(f"⚠️  Product not found: {product_data['id']}")
        
        # Restore category URLs
        for category_data in backup_data.get('categories', []):
            try:
                category = Category.objects.get(key=category_data['key'])
                if not category.image_url:  # Only restore if empty
                    category.image_url = category_data['image_url']
                    category.save(update_fields=['image_url'])
                    restored_count += 1
                    self.stdout.write(f"✅ Restored category: {category.label}")
            except Category.DoesNotExist:
                self.stdout.write(f"⚠️  Category not found: {category_data['key']}")
        
        # Restore product image URLs
        for img_data in backup_data.get('product_images', []):
            try:
                # Try to find existing image or create new one
                try:
                    img = ProductImage.objects.get(id=img_data['id'])
                except ProductImage.DoesNotExist:
                    # Create new image if it doesn't exist
                    try:
                        product = Product.objects.get(id=img_data['product_id'])
                        img = ProductImage.objects.create(
                            product=product,
                            image_url=img_data['image_url'],
                            is_primary=img_data.get('is_primary', False),
                            order=img_data.get('order', 0)
                        )
                        restored_count += 1
                        self.stdout.write(f"✅ Created product image for: {product.title}")
                        continue
                    except Product.DoesNotExist:
                        self.stdout.write(f"⚠️  Product not found for image: {img_data['product_id']}")
                        continue
                
                if not img.image_url:  # Only restore if empty
                    img.image_url = img_data['image_url']
                    img.save(update_fields=['image_url'])
                    restored_count += 1
                    self.stdout.write(f"✅ Restored product image: {img.product.title}")
                    
            except Exception as e:
                self.stdout.write(f"❌ Error restoring image {img_data['id']}: {e}")
        
        self.stdout.write(
            self.style.SUCCESS(f"✅ Restoration complete! Restored {restored_count} URLs")
        )
        return True