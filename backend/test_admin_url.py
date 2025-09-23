#!/usr/bin/env python
"""
Test the specific admin URL that's causing 500 errors
"""
import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def test_admin_urls():
    """Test admin URLs that might be causing 500 errors"""
    
    # Create a test client
    client = Client()
    
    # Get or create a superuser for testing
    User = get_user_model()
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No admin user found. Creating test admin...")
            admin_user = User.objects.create_superuser(
                username='testadmin',
                email='test@example.com',
                password='testpass123'
            )
        
        # Login as admin
        client.force_login(admin_user)
        print(f"✅ Logged in as admin: {admin_user.username}")
        
    except Exception as e:
        print(f"❌ Failed to create/login admin user: {e}")
        return
    
    # Test URLs that might be failing
    test_urls = [
        '/admin/',
        '/admin/shop/',
        '/admin/shop/orderitem/',
        '/admin/shop/order/',
        '/admin/shop/product/',
    ]
    
    for url in test_urls:
        try:
            print(f"\n🧪 Testing URL: {url}")
            response = client.get(url)
            
            if response.status_code == 200:
                print(f"✅ {url} - OK (200)")
            elif response.status_code == 302:
                print(f"🔄 {url} - Redirect (302)")
            else:
                print(f"❌ {url} - Error ({response.status_code})")
                if hasattr(response, 'content'):
                    content = response.content.decode('utf-8')[:500]
                    print(f"   Content preview: {content}")
                    
        except Exception as e:
            print(f"❌ {url} - Exception: {e}")
            import traceback
            traceback.print_exc()

def main():
    print("🔍 Testing Admin URLs")
    print("=" * 50)
    
    test_admin_urls()
    
    print("\n✅ Admin URL testing completed!")

if __name__ == '__main__':
    main()