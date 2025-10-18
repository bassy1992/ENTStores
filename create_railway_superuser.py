#!/usr/bin/env python
"""
Railway Superuser Creation Script
This script creates a Django superuser for Railway deployment.
Run this after deploying to Railway to create an admin user.
"""

import os
import sys
import django
from django.conf import settings

def create_superuser():
    """Create or update superuser for Railway deployment"""
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    django.setup()
    
    from django.contrib.auth.models import User
    
    # Get credentials from environment or use defaults
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@entstore.com')
    password = os.environ.get('ADMIN_PASSWORD', 'EntStore2024!')
    
    print("🚂 Railway Superuser Creation")
    print("=" * 40)
    print(f"Username: {username}")
    print(f"Email: {email}")
    print("=" * 40)
    
    try:
        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            print(f"⚠️  Superuser '{username}' already exists")
            
            # Update existing user
            user = User.objects.get(username=username)
            user.email = email
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            
            print(f"✅ Updated existing superuser '{username}'")
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
            
        else:
            # Create new superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            
            print(f"✅ Created new superuser '{username}'")
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
        
        print("\n🎉 Superuser setup complete!")
        print(f"🌐 Access admin at: https://your-app.up.railway.app/admin/")
        print(f"👤 Login with: {username} / {password}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

if __name__ == '__main__':
    success = create_superuser()
    sys.exit(0 if success else 1)