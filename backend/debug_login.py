#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Debug login process
try:
    print("=== LOGIN DEBUG ===")
    
    # Check if user exists
    try:
        user = User.objects.get(username='admin')
        print(f"✅ User found: {user.username}")
        print(f"📧 Email: {user.email}")
        print(f"👤 Is superuser: {user.is_superuser}")
        print(f"👨‍💼 Is staff: {user.is_staff}")
        print(f"✅ Is active: {user.is_active}")
        print(f"🔑 Has usable password: {user.has_usable_password()}")
        
        # Test password directly
        if user.check_password('password123'):
            print("✅ Direct password check: SUCCESS")
        else:
            print("❌ Direct password check: FAILED")
            
        # Test Django authentication
        auth_user = authenticate(username='admin', password='password123')
        if auth_user:
            print("✅ Django authenticate: SUCCESS")
            print(f"   Authenticated user: {auth_user.username}")
        else:
            print("❌ Django authenticate: FAILED")
            
        # Check database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user WHERE username = 'admin'")
            count = cursor.fetchone()[0]
            print(f"✅ Database query result: {count} admin users found")
            
    except User.DoesNotExist:
        print("❌ User 'admin' not found in database")
        
    # List all users
    print("\n=== ALL USERS ===")
    users = User.objects.all()
    for user in users:
        print(f"Username: {user.username}, Active: {user.is_active}, Staff: {user.is_staff}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()