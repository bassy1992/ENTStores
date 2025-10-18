#!/usr/bin/env python
"""
Railway startup script to ensure proper deployment
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def railway_startup():
    """Complete Railway startup process"""
    
    print("🚂 Starting Railway deployment process...")
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    django.setup()
    
    try:
        # 1. Run migrations
        print("📦 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed")
        
        # 2. Collect static files
        print("📁 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected")
        
        # 3. Test database connection
        print("🔍 Testing database connection...")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Database connection successful: {result}")
        
        # 4. Create superuser if needed
        print("👤 Setting up superuser...")
        from django.contrib.auth.models import User
        
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'Enontinoclothing@gmail.com')
        password = os.environ.get('ADMIN_PASSWORD', 'EntStore2024!')
        
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.email = email
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"✅ Updated existing superuser '{username}'")
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            print(f"✅ Created new superuser '{username}'")
        
        # 5. Test key endpoints
        print("🔍 Testing key endpoints...")
        from django.test import Client
        client = Client()
        
        # Test health endpoint
        try:
            response = client.get('/api/health/')
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"⚠️  Health endpoint returned {response.status_code}")
        except Exception as e:
            print(f"⚠️  Health endpoint test failed: {e}")
        
        # Test products endpoint
        try:
            response = client.get('/api/shop/products/')
            if response.status_code == 200:
                print("✅ Products endpoint working")
            else:
                print(f"⚠️  Products endpoint returned {response.status_code}")
        except Exception as e:
            print(f"⚠️  Products endpoint test failed: {e}")
        
        print("🎉 Railway startup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Railway startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = railway_startup()
    sys.exit(0 if success else 1)