#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

# Delete all users and create fresh admin
try:
    # Delete all existing users
    User.objects.all().delete()
    print("✅ Deleted all existing users")
    
    # Create fresh superuser
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='password123'
    )
    
    # Verify user was created
    print(f"✅ Created superuser: {user.username}")
    print(f"📧 Email: {user.email}")
    print(f"🔑 Password: password123")
    print(f"👤 Is superuser: {user.is_superuser}")
    print(f"👨‍💼 Is staff: {user.is_staff}")
    print(f"✅ Is active: {user.is_active}")
    
    # Test password
    if user.check_password('password123'):
        print("✅ Password verification successful")
    else:
        print("❌ Password verification failed")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()