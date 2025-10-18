"""
Django management command to backup media URLs
This runs automatically before Railway deployments
"""
import os
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from shop.models import Product, Category, ProductImage


class Command(BaseCommand):
    help = 'Backup media URLs to file and environment variables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default=None,
            help='Output file path (default: auto-generated)',
        )
        parser.add_argument(
            '--env-format',
            action='store_true',
            help='Also output environment variable format',
        )

    def handle(self, *args, **options):
        self.stdout.write("🔄 Starting media URL backup...")
        
        # Collect all media URLs
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'products': [],
            'categories': [],
            'product_images': []
        }
        
        # Backup product URLs
        products = Product.objects.filter(image_url__isnull=False).exclude(image_url='')
        for product in products:
            backup_data['products'].append({
                'id': product.id,
                'title': product.title,
                'image_url': product.image_url
            })
        
        # Backup category URLs
        categories = Category.objects.filter(image_url__isnull=False).exclude(image_url='')
        for category in categories:
            backup_data['categories'].append({
                'key': category.key,
                'label': category.label,
                'image_url': category.image_url
            })
        
        # Backup product image URLs
        product_images = ProductImage.objects.filter(image_url__isnull=False).exclude(image_url='')
        for img in product_images:
            backup_data['product_images'].append({
                'id': img.id,
                'product_id': img.product.id,
                'image_url': img.image_url,
                'is_primary': img.is_primary,
                'order': img.order
            })
        
        # Generate output filename
        if options['output']:
            backup_filename = options['output']
        else:
            backup_filename = f"media_urls_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Save backup file
        try:
            with open(backup_filename, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2)
            
            self.stdout.write(f"✅ Backup saved to: {backup_filename}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to save backup: {e}"))
            return
        
        # Output statistics
        total_urls = len(backup_data['products']) + len(backup_data['categories']) + len(backup_data['product_images'])
        self.stdout.write(f"📊 Backed up {total_urls} URLs:")
        self.stdout.write(f"   - Products: {len(backup_data['products'])}")
        self.stdout.write(f"   - Categories: {len(backup_data['categories'])}")
        self.stdout.write(f"   - Product Images: {len(backup_data['product_images'])}")
        
        # Generate environment variable format if requested
        if options['env_format']:
            self.generate_env_format(backup_data)
        
        self.stdout.write(self.style.SUCCESS("✅ Backup completed successfully"))

    def generate_env_format(self, backup_data):
        """Generate environment variable format"""
        env_vars = {}
        
        # Product URLs
        for product in backup_data['products']:
            env_vars[f"PRODUCT_IMG_{product['id']}"] = product['image_url']
        
        # Category URLs
        for category in backup_data['categories']:
            env_vars[f"CATEGORY_IMG_{category['key']}"] = category['image_url']
        
        # Product image URLs
        for img in backup_data['product_images']:
            env_vars[f"PRODIMG_{img['id']}"] = img['image_url']
        
        # Save environment variable format
        env_filename = f"media_urls_env_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(env_filename, 'w', encoding='utf-8') as f:
                json.dump(env_vars, f, indent=2)
            
            self.stdout.write(f"📄 Environment variables saved to: {env_filename}")
            
            # Also create a shell script for easy setting
            shell_filename = f"set_media_env_vars_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sh"
            with open(shell_filename, 'w', encoding='utf-8') as f:
                f.write("#!/bin/bash\n")
                f.write("# Set media URL environment variables in Railway\n")
                f.write("echo 'Setting media URL environment variables...'\n\n")
                
                for key, value in env_vars.items():
                    # Escape quotes in the value
                    escaped_value = value.replace('"', '\\"')
                    f.write(f'railway variables set {key}="{escaped_value}"\n')
                
                f.write(f"\necho 'Set {len(env_vars)} environment variables'\n")
            
            # Make shell script executable
            os.chmod(shell_filename, 0o755)
            self.stdout.write(f"🔧 Shell script created: {shell_filename}")
            
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"⚠️  Failed to create env format: {e}"))