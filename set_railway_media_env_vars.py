#!/usr/bin/env python3
"""
Set Railway Environment Variables for Media URLs
This stores your media URLs as environment variables so they persist across deployments
"""
import os
import sys
import json
import subprocess

# Add Django setup
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from shop.models import Product, Category, ProductImage

def get_current_media_urls():
    """Get all current media URLs from database"""
    media_data = {}
    
    # Get product URLs
    products = Product.objects.filter(image_url__isnull=False).exclude(image_url='')
    for product in products:
        media_data[f"PRODUCT_IMG_{product.id}"] = product.image_url
    
    # Get category URLs
    categories = Category.objects.filter(image_url__isnull=False).exclude(image_url='')
    for category in categories:
        media_data[f"CATEGORY_IMG_{category.key}"] = category.image_url
    
    # Get product image URLs
    images = ProductImage.objects.filter(image_url__isnull=False).exclude(image_url='')
    for img in images:
        media_data[f"PRODIMG_{img.id}"] = img.image_url
    
    return media_data

def set_railway_env_vars(media_data):
    """Set environment variables in Railway"""
    print(f"🔄 Setting {len(media_data)} environment variables in Railway...")
    
    success_count = 0
    for key, value in media_data.items():
        try:
            # Use railway CLI to set environment variable
            result = subprocess.run([
                'railway', 'variables', 'set', f'{key}={value}'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                success_count += 1
                print(f"✅ Set {key}")
            else:
                print(f"❌ Failed to set {key}: {result.stderr}")
        except Exception as e:
            print(f"❌ Error setting {key}: {e}")
    
    print(f"✅ Successfully set {success_count}/{len(media_data)} environment variables")
    return success_count

def create_restore_from_env_script():
    """Create script to restore URLs from environment variables"""
    script_content = '''#!/usr/bin/env python3
"""
Restore media URLs from Railway environment variables
Run this after deployment to restore all media URLs
"""
import os
import sys

# Add Django setup
sys.path.append('/app/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from shop.models import Product, Category, ProductImage

def restore_media_urls_from_env():
    """Restore media URLs from environment variables"""
    restored_count = 0
    
    # Restore product URLs
    for key, value in os.environ.items():
        if key.startswith('PRODUCT_IMG_'):
            product_id = key.replace('PRODUCT_IMG_', '')
            try:
                product = Product.objects.get(id=product_id)
                if not product.image_url or product.image_url != value:
                    product.image_url = value
                    product.save(update_fields=['image_url'])
                    restored_count += 1
                    print(f"✅ Restored product: {product.title}")
            except Product.DoesNotExist:
                print(f"⚠️  Product not found: {product_id}")
        
        elif key.startswith('CATEGORY_IMG_'):
            category_key = key.replace('CATEGORY_IMG_', '')
            try:
                category = Category.objects.get(key=category_key)
                if not category.image_url or category.image_url != value:
                    category.image_url = value
                    category.save(update_fields=['image_url'])
                    restored_count += 1
                    print(f"✅ Restored category: {category.label}")
            except Category.DoesNotExist:
                print(f"⚠️  Category not found: {category_key}")
        
        elif key.startswith('PRODIMG_'):
            img_id = key.replace('PRODIMG_', '')
            try:
                img = ProductImage.objects.get(id=img_id)
                if not img.image_url or img.image_url != value:
                    img.image_url = value
                    img.save(update_fields=['image_url'])
                    restored_count += 1
                    print(f"✅ Restored product image: {img.product.title}")
            except ProductImage.DoesNotExist:
                print(f"⚠️  Product image not found: {img_id}")
    
    print(f"\\n✅ Restored {restored_count} media URLs from environment variables")
    return restored_count

if __name__ == "__main__":
    print("🔄 Restoring media URLs from Railway environment variables...")
    restore_media_urls_from_env()
'''
    
    with open('restore_from_railway_env.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Created restore_from_railway_env.py")

def main():
    """Main function"""
    print("🔧 Railway Media URL Environment Variable Setup")
    print("=" * 50)
    
    # Get current media URLs
    media_data = get_current_media_urls()
    print(f"📊 Found {len(media_data)} media URLs to preserve")
    
    if not media_data:
        print("❌ No media URLs found in database")
        return
    
    # Show sample URLs
    print("\\n📸 Sample URLs:")
    for i, (key, value) in enumerate(list(media_data.items())[:3]):
        print(f"   {key}: {value}")
    
    # Ask for confirmation
    proceed = input(f"\\n🤔 Set {len(media_data)} environment variables in Railway? (y/n): ").lower().strip()
    
    if proceed == 'y':
        # Check if railway CLI is available
        try:
            result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Railway CLI not found. Install it from: https://docs.railway.app/develop/cli")
                return
        except Exception:
            print("❌ Railway CLI not found. Install it from: https://docs.railway.app/develop/cli")
            return
        
        # Set environment variables
        success_count = set_railway_env_vars(media_data)
        
        if success_count > 0:
            print(f"\\n🎉 Successfully configured {success_count} environment variables!")
            print("\\n📝 Next steps:")
            print("1. Deploy to Railway: railway up")
            print("2. After deployment, run: python restore_from_railway_env.py")
        else:
            print("❌ Failed to set environment variables")
    else:
        print("📝 Manual setup:")
        print("1. Go to Railway dashboard > Your project > Variables")
        print("2. Add these environment variables:")
        for key, value in list(media_data.items())[:5]:
            print(f"   {key} = {value}")
        if len(media_data) > 5:
            print(f"   ... and {len(media_data) - 5} more")
    
    # Always create the restore script
    create_restore_from_env_script()

if __name__ == "__main__":
    main()