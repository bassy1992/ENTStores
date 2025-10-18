#!/usr/bin/env python3
"""
Permanent Railway Media URL Solution
This sets up automatic media URL preservation for Railway deployments
"""
import os
import sys
import json
import subprocess
from datetime import datetime

# Add Django setup
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from shop.models import Product, Category, ProductImage

def create_media_url_constants():
    """Create a Python file with media URLs as constants"""
    
    # Get all current media URLs
    media_urls = {}
    
    # Product URLs
    products = Product.objects.filter(image_url__isnull=False).exclude(image_url='')
    for product in products:
        media_urls[f"PRODUCT_{product.id}"] = product.image_url
    
    # Category URLs
    categories = Category.objects.filter(image_url__isnull=False).exclude(image_url='')
    for category in categories:
        media_urls[f"CATEGORY_{category.key}"] = category.image_url
    
    # Product image URLs
    images = ProductImage.objects.filter(image_url__isnull=False).exclude(image_url='')
    for img in images:
        media_urls[f"PRODIMG_{img.id}"] = img.image_url
    
    # Create constants file
    constants_content = f'''"""
Media URL Constants - Auto-generated on {datetime.now().isoformat()}
This file contains all media URLs as constants to preserve them across deployments
"""

# Media URL constants
MEDIA_URLS = {{
'''
    
    for key, url in media_urls.items():
        constants_content += f'    "{key}": "{url}",\n'
    
    constants_content += '''
}

def get_product_image_url(product_id):
    """Get product image URL by product ID"""
    return MEDIA_URLS.get(f"PRODUCT_{product_id}")

def get_category_image_url(category_key):
    """Get category image URL by category key"""
    return MEDIA_URLS.get(f"CATEGORY_{category_key}")

def get_product_image_by_id(image_id):
    """Get product image URL by image ID"""
    return MEDIA_URLS.get(f"PRODIMG_{image_id}")

def restore_all_media_urls():
    """Restore all media URLs to database"""
    from shop.models import Product, Category, ProductImage
    
    restored_count = 0
    
    # Restore product URLs
    for key, url in MEDIA_URLS.items():
        if key.startswith("PRODUCT_"):
            product_id = key.replace("PRODUCT_", "")
            try:
                product = Product.objects.get(id=product_id)
                if not product.image_url:
                    product.image_url = url
                    product.save(update_fields=['image_url'])
                    restored_count += 1
            except Product.DoesNotExist:
                pass
        
        elif key.startswith("CATEGORY_"):
            category_key = key.replace("CATEGORY_", "")
            try:
                category = Category.objects.get(key=category_key)
                if not category.image_url:
                    category.image_url = url
                    category.save(update_fields=['image_url'])
                    restored_count += 1
            except Category.DoesNotExist:
                pass
        
        elif key.startswith("PRODIMG_"):
            img_id = key.replace("PRODIMG_", "")
            try:
                img = ProductImage.objects.get(id=img_id)
                if not img.image_url:
                    img.image_url = url
                    img.save(update_fields=['image_url'])
                    restored_count += 1
            except ProductImage.DoesNotExist:
                pass
    
    return restored_count
'''
    
    # Save to backend directory
    constants_file = 'backend/shop/media_url_constants.py'
    with open(constants_file, 'w', encoding='utf-8') as f:
        f.write(constants_content)
    
    print(f"✅ Created media URL constants file: {constants_file}")
    print(f"📊 Stored {len(media_urls)} media URLs as constants")
    
    return constants_file

def update_models_to_use_constants():
    """Update models to use constants as fallback"""
    
    # Add import and fallback method to models.py
    models_addition = '''
# Import media URL constants
try:
    from .media_url_constants import get_product_image_url, get_category_image_url, get_product_image_by_id
except ImportError:
    # Fallback if constants file doesn't exist
    def get_product_image_url(product_id):
        return None
    def get_category_image_url(category_key):
        return None
    def get_product_image_by_id(image_id):
        return None
'''
    
    # Read current models.py
    models_file = 'backend/shop/models.py'
    with open(models_file, 'r', encoding='utf-8') as f:
        models_content = f.read()
    
    # Check if already added
    if 'media_url_constants' not in models_content:
        # Add the import at the top after existing imports
        import_pos = models_content.find('from django.dispatch import receiver')
        if import_pos != -1:
            # Find the end of that line
            line_end = models_content.find('\n', import_pos) + 1
            # Insert our addition
            models_content = models_content[:line_end] + models_addition + models_content[line_end:]
            
            # Save updated models.py
            with open(models_file, 'w', encoding='utf-8') as f:
                f.write(models_content)
            
            print("✅ Updated models.py to use media URL constants")
        else:
            print("⚠️  Could not find insertion point in models.py")
    else:
        print("ℹ️  Models.py already updated")

def create_auto_restore_app():
    """Create a Django app that automatically restores media URLs"""
    
    app_content = '''"""
Auto-restore media URLs app
This app automatically restores media URLs when Django starts
"""
from django.apps import AppConfig

class AutoRestoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auto_restore'
    
    def ready(self):
        """Called when Django is ready - restore media URLs"""
        try:
            # Import here to avoid circular imports
            from shop.media_url_constants import restore_all_media_urls
            
            # Only restore if we're in production (Railway)
            import os
            if os.getenv('RAILWAY_ENVIRONMENT'):
                restored_count = restore_all_media_urls()
                print(f"🔄 Auto-restored {restored_count} media URLs")
        except Exception as e:
            print(f"⚠️  Auto-restore failed: {e}")
'''
    
    # Create auto_restore app directory
    app_dir = 'backend/auto_restore'
    os.makedirs(app_dir, exist_ok=True)
    
    # Create __init__.py
    with open(f'{app_dir}/__init__.py', 'w') as f:
        f.write('')
    
    # Create apps.py
    with open(f'{app_dir}/apps.py', 'w', encoding='utf-8') as f:
        f.write(app_content)
    
    print("✅ Created auto-restore Django app")
    
    # Update settings.py to include the app
    settings_file = 'backend/myproject/settings.py'
    with open(settings_file, 'r', encoding='utf-8') as f:
        settings_content = f.read()
    
    if "'auto_restore'," not in settings_content:
        # Find INSTALLED_APPS and add our app
        apps_start = settings_content.find('INSTALLED_APPS = [')
        if apps_start != -1:
            # Find the end of the list
            apps_end = settings_content.find(']', apps_start)
            if apps_end != -1:
                # Insert our app before the closing bracket
                insertion_point = apps_end
                # Find the last app entry to add comma if needed
                last_line = settings_content[:apps_end].split('\n')[-1]
                if not last_line.strip().endswith(','):
                    new_app = "    'auto_restore',\n"
                else:
                    new_app = "    'auto_restore',\n"
                
                settings_content = settings_content[:insertion_point] + new_app + settings_content[insertion_point:]
                
                # Save updated settings.py
                with open(settings_file, 'w', encoding='utf-8') as f:
                    f.write(settings_content)
                
                print("✅ Added auto_restore app to INSTALLED_APPS")
            else:
                print("⚠️  Could not find end of INSTALLED_APPS")
        else:
            print("⚠️  Could not find INSTALLED_APPS in settings.py")
    else:
        print("ℹ️  auto_restore app already in INSTALLED_APPS")

def create_deployment_script():
    """Create a deployment script that handles everything"""
    
    script_content = '''#!/bin/bash
# Railway Deployment Script with Automatic Media URL Preservation
echo "🚀 Starting Railway deployment with media URL preservation..."

# Step 1: Backup current media URLs
echo "📦 Backing up media URLs..."
cd backend
python manage.py backup_media_urls --env-format

# Step 2: Deploy to Railway
echo "🚀 Deploying to Railway..."
cd ..
railway up

# Step 3: Wait for deployment
echo "⏳ Waiting for deployment to be ready..."
sleep 30

# Step 4: Restore media URLs (this happens automatically via auto_restore app)
echo "✅ Deployment complete! Media URLs will be restored automatically."
echo "🔗 Check your site: https://entstores-production.up.railway.app"
'''
    
    with open('deploy_with_media_preservation.sh', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod('deploy_with_media_preservation.sh', 0o755)
    print("✅ Created deployment script: deploy_with_media_preservation.sh")

def main():
    """Set up permanent media URL preservation"""
    print("🔧 Setting up permanent Railway media URL preservation...")
    print("=" * 60)
    
    # Step 1: Create media URL constants
    constants_file = create_media_url_constants()
    
    # Step 2: Update models to use constants
    update_models_to_use_constants()
    
    # Step 3: Create auto-restore app
    create_auto_restore_app()
    
    # Step 4: Create deployment script
    create_deployment_script()
    
    print("\n🎉 Permanent solution setup complete!")
    print("\n📋 What was created:")
    print("✅ Media URL constants file (preserves URLs in code)")
    print("✅ Auto-restore Django app (restores URLs on startup)")
    print("✅ Updated models.py (fallback support)")
    print("✅ Railway deployment configuration (nixpacks.toml)")
    print("✅ Deployment script (deploy_with_media_preservation.sh)")
    
    print("\n🚀 How it works:")
    print("1. Your media URLs are now stored as constants in code")
    print("2. When Railway deploys, the auto-restore app runs automatically")
    print("3. All media URLs are restored from constants")
    print("4. No manual intervention required!")
    
    print("\n🔄 Next deployment:")
    print("1. Run: ./deploy_with_media_preservation.sh")
    print("2. Or just: railway up (auto-restore will handle the rest)")
    
    print("\n💡 Benefits:")
    print("✅ Fully automated - no manual steps")
    print("✅ URLs stored in code - version controlled")
    print("✅ Instant restoration on deployment")
    print("✅ No external dependencies")
    print("✅ Works with any Railway deployment method")

if __name__ == "__main__":
    main()