#!/usr/bin/env python
"""
Test Django startup for Railway deployment
"""

import os
import sys
import django
from django.conf import settings

def test_django_startup():
    """Test if Django can start properly"""
    
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
        django.setup()
        
        print("✅ Django setup successful")
        
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Database connection successful: {result}")
        
        # Test if we can import views
        from shop import views
        print("✅ Shop views import successful")
        
        # Test URL resolution
        from django.urls import reverse
        try:
            health_url = reverse('health-check')
            print(f"✅ Health check URL resolved: {health_url}")
        except Exception as e:
            print(f"⚠️  Health check URL resolution failed: {e}")
        
        try:
            products_url = reverse('shop:product-list')
            print(f"✅ Products URL resolved: {products_url}")
        except Exception as e:
            print(f"⚠️  Products URL resolution failed: {e}")
        
        print("🎉 Django startup test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Django startup test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_django_startup()
    sys.exit(0 if success else 1)