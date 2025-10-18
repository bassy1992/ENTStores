#!/usr/bin/env python3
"""
Pre-deployment script for Railway
Automatically backs up Digital Ocean URLs before deployment
"""
import os
import sys
import json
import requests
from datetime import datetime

def backup_urls_to_railway_env():
    """Backup URLs as Railway environment variables"""
    try:
        # Test Railway API connection
        response = requests.get("https://entstores-production.up.railway.app/api/shop/products/", timeout=10)
        if response.status_code != 200:
            print("❌ Cannot connect to Railway API")
            return False
        
        data = response.json()
        products = data.get('results', [])
        
        # Create backup data
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'products': []
        }
        
        for product in products:
            if product.get('image_url'):
                backup_data['products'].append({
                    'id': product['id'],
                    'title': product['title'],
                    'image_url': product['image_url']
                })
        
        # Save to file
        backup_filename = f"media_urls_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2)
        
        print(f"✅ Backed up {len(backup_data['products'])} product URLs to {backup_filename}")
        
        # Also save as environment variable format
        env_backup = {}
        for i, product in enumerate(backup_data['products']):
            env_backup[f"PRODUCT_URL_{i}"] = f"{product['id']}|{product['image_url']}"
        
        with open('media_urls_env_backup.json', 'w', encoding='utf-8') as f:
            json.dump(env_backup, f, indent=2)
        
        print(f"✅ Created environment variable backup")
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def create_restore_script():
    """Create a script that can restore URLs from environment variables"""
    script_content = '''#!/usr/bin/env python3
"""
Restore Digital Ocean URLs from backup
Run this after Railway deployment
"""
import os
import sys
import json

# Add Django setup
sys.path.append('/app/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

from shop.models import Product

def restore_from_env_backup():
    """Restore URLs from environment backup file"""
    try:
        if os.path.exists('media_urls_env_backup.json'):
            with open('media_urls_env_backup.json', 'r') as f:
                env_data = json.load(f)
            
            restored = 0
            for key, value in env_data.items():
                if key.startswith('PRODUCT_URL_'):
                    product_id, image_url = value.split('|', 1)
                    try:
                        product = Product.objects.get(id=product_id)
                        if not product.image_url:
                            product.image_url = image_url
                            product.save(update_fields=['image_url'])
                            restored += 1
                            print(f"✅ Restored: {product.title}")
                    except Product.DoesNotExist:
                        print(f"⚠️  Product not found: {product_id}")
            
            print(f"✅ Restored {restored} product URLs")
            return True
        else:
            print("❌ No environment backup file found")
            return False
            
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False

if __name__ == "__main__":
    restore_from_env_backup()
'''
    
    with open('restore_media_urls.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print("✅ Created restore_media_urls.py script")

if __name__ == "__main__":
    print("🔄 Pre-deployment backup starting...")
    success = backup_urls_to_railway_env()
    create_restore_script()
    
    if success:
        print("\n💡 After Railway deployment, run:")
        print("   python restore_media_urls.py")
    else:
        print("\n❌ Backup failed - check your Railway connection")