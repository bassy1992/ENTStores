#!/usr/bin/env python3
"""
Backup and Restore Digital Ocean Media URLs
This script helps preserve your Digital Ocean URLs during Railway deployments
"""
import os
import sys
import json
import requests
from datetime import datetime

# Add Django setup
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from shop.models import Product, Category, ProductImage

def backup_media_urls():
    """Backup all Digital Ocean URLs from the database"""
    backup_data = {
        'timestamp': datetime.now().isoformat(),
        'products': [],
        'categories': [],
        'product_images': []
    }
    
    print("🔄 Backing up Digital Ocean URLs...")
    
    # Backup product URLs
    products = Product.objects.all()
    for product in products:
        if product.image_url:
            backup_data['products'].append({
                'id': product.id,
                'title': product.title,
                'image_url': product.image_url
            })
    
    # Backup category URLs
    categories = Category.objects.all()
    for category in categories:
        if category.image_url:
            backup_data['categories'].append({
                'key': category.key,
                'label': category.label,
                'image_url': category.image_url
            })
    
    # Backup product image URLs
    product_images = ProductImage.objects.all()
    for img in product_images:
        if img.image_url:
            backup_data['product_images'].append({
                'id': img.id,
                'product_id': img.product.id,
                'image_url': img.image_url,
                'is_primary': img.is_primary,
                'order': img.order
            })
    
    # Save backup file
    backup_filename = f"media_urls_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_filename, 'w') as f:
        json.dump(backup_data, f, indent=2)
    
    print(f"✅ Backup saved to: {backup_filename}")
    print(f"📊 Backed up:")
    print(f"   - Products: {len(backup_data['products'])}")
    print(f"   - Categories: {len(backup_data['categories'])}")
    print(f"   - Product Images: {len(backup_data['product_images'])}")
    
    return backup_filename

def restore_media_urls(backup_file):
    """Restore Digital Ocean URLs from backup file"""
    if not os.path.exists(backup_file):
        print(f"❌ Backup file not found: {backup_file}")
        return False
    
    print(f"🔄 Restoring URLs from: {backup_file}")
    
    with open(backup_file, 'r') as f:
        backup_data = json.load(f)
    
    restored_count = 0
    
    # Restore product URLs
    for product_data in backup_data['products']:
        try:
            product = Product.objects.get(id=product_data['id'])
            if not product.image_url:  # Only restore if empty
                product.image_url = product_data['image_url']
                product.save(update_fields=['image_url'])
                restored_count += 1
                print(f"✅ Restored product: {product.title}")
        except Product.DoesNotExist:
            print(f"⚠️  Product not found: {product_data['id']} - {product_data['title']}")
    
    # Restore category URLs
    for category_data in backup_data['categories']:
        try:
            category = Category.objects.get(key=category_data['key'])
            if not category.image_url:  # Only restore if empty
                category.image_url = category_data['image_url']
                category.save(update_fields=['image_url'])
                restored_count += 1
                print(f"✅ Restored category: {category.label}")
        except Category.DoesNotExist:
            print(f"⚠️  Category not found: {category_data['key']} - {category_data['label']}")
    
    # Restore product image URLs
    for img_data in backup_data['product_images']:
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
                        is_primary=img_data['is_primary'],
                        order=img_data['order']
                    )
                    restored_count += 1
                    print(f"✅ Created product image for: {product.title}")
                    continue
                except Product.DoesNotExist:
                    print(f"⚠️  Product not found for image: {img_data['product_id']}")
                    continue
            
            if not img.image_url:  # Only restore if empty
                img.image_url = img_data['image_url']
                img.save(update_fields=['image_url'])
                restored_count += 1
                print(f"✅ Restored product image: {img.product.title}")
                
        except Exception as e:
            print(f"❌ Error restoring image {img_data['id']}: {e}")
    
    print(f"✅ Restoration complete! Restored {restored_count} URLs")
    return True

def check_current_urls():
    """Check current state of URLs in database"""
    print("🔍 Checking current URL status...")
    
    products_with_urls = Product.objects.filter(image_url__isnull=False).exclude(image_url='')
    categories_with_urls = Category.objects.filter(image_url__isnull=False).exclude(image_url='')
    images_with_urls = ProductImage.objects.filter(image_url__isnull=False).exclude(image_url='')
    
    print(f"📊 Current status:")
    print(f"   - Products with URLs: {products_with_urls.count()}")
    print(f"   - Categories with URLs: {categories_with_urls.count()}")
    print(f"   - Product Images with URLs: {images_with_urls.count()}")
    
    # Show some examples
    if products_with_urls.exists():
        print(f"\n📸 Sample product URLs:")
        for product in products_with_urls[:3]:
            print(f"   - {product.title}: {product.image_url}")
    
    return {
        'products': products_with_urls.count(),
        'categories': categories_with_urls.count(),
        'images': images_with_urls.count()
    }

def test_digital_ocean_urls():
    """Test if Digital Ocean URLs are accessible"""
    print("🌐 Testing Digital Ocean URL accessibility...")
    
    products = Product.objects.filter(image_url__isnull=False).exclude(image_url='')[:5]
    working_urls = 0
    broken_urls = 0
    
    for product in products:
        try:
            response = requests.head(product.image_url, timeout=5)
            if response.status_code == 200:
                working_urls += 1
                print(f"✅ {product.title}: Working")
            else:
                broken_urls += 1
                print(f"❌ {product.title}: Status {response.status_code}")
        except Exception as e:
            broken_urls += 1
            print(f"❌ {product.title}: {str(e)}")
    
    print(f"\n📊 URL Test Results:")
    print(f"   - Working URLs: {working_urls}")
    print(f"   - Broken URLs: {broken_urls}")
    
    return working_urls, broken_urls

def create_railway_deployment_script():
    """Create a script to run after Railway deployment"""
    script_content = '''#!/usr/bin/env python3
"""
Post-deployment script for Railway
Automatically restores Digital Ocean URLs after deployment
"""
import os
import sys
import json
from pathlib import Path

# Add Django setup
sys.path.append('/app/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

def restore_from_latest_backup():
    """Find and restore from the latest backup"""
    backup_files = list(Path('.').glob('media_urls_backup_*.json'))
    if not backup_files:
        print("No backup files found")
        return
    
    latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
    print(f"Restoring from: {latest_backup}")
    
    # Import and run restore function
    from backup_restore_media_urls import restore_media_urls
    restore_media_urls(str(latest_backup))

if __name__ == "__main__":
    restore_from_latest_backup()
'''
    
    with open('railway_post_deploy.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Created railway_post_deploy.py script")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Backup and restore Digital Ocean media URLs')
    parser.add_argument('action', choices=['backup', 'restore', 'check', 'test'], 
                       help='Action to perform')
    parser.add_argument('--file', help='Backup file to restore from')
    
    args = parser.parse_args()
    
    if args.action == 'backup':
        backup_file = backup_media_urls()
        print(f"\n💡 To restore after Railway deployment:")
        print(f"   python backup_restore_media_urls.py restore --file {backup_file}")
        
    elif args.action == 'restore':
        if not args.file:
            # Find latest backup
            import glob
            backups = glob.glob('media_urls_backup_*.json')
            if backups:
                latest = max(backups, key=os.path.getctime)
                print(f"Using latest backup: {latest}")
                restore_media_urls(latest)
            else:
                print("❌ No backup file specified and no backups found")
        else:
            restore_media_urls(args.file)
            
    elif args.action == 'check':
        check_current_urls()
        
    elif args.action == 'test':
        test_digital_ocean_urls()
    
    # Always create the deployment script
    create_railway_deployment_script()

if __name__ == "__main__":
    main()