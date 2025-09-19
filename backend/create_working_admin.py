#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

# Create a working admin user
try:
    # Delete existing admin users
    User.objects.filter(username='admin').delete()
    print("✅ Deleted existing admin users")
    
    # Create new admin with very simple credentials
    user = User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='admin'
    )
    
    # Make user superuser and staff
    user.is_superuser = True
    user.is_staff = True
    user.is_active = True
    user.save()
    
    print(f"✅ Created admin user: {user.username}")
    print(f"📧 Email: {user.email}")
    print(f"🔑 Password: admin")
    print(f"👤 Is superuser: {user.is_superuser}")
    print(f"👨‍💼 Is staff: {user.is_staff}")
    print(f"✅ Is active: {user.is_active}")
    
    # Test the password
    if user.check_password('admin'):
        print("✅ Password test: SUCCESS")
    else:
        print("❌ Password test: FAILED")
        
    print("\n🎯 LOGIN CREDENTIALS:")
    print("Username: admin")
    print("Password: admin")
    print("URL: https://enontino-production.up.railway.app/admin/")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()