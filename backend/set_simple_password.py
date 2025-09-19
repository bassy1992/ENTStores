#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

# Set simple password
try:
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    print(f"✅ Password updated for user: {user.username}")
    print(f"📧 Email: {user.email}")
    print(f"🔑 New password: admin123")
    
except User.DoesNotExist:
    print("❌ User 'admin' not found")
except Exception as e:
    print(f"❌ Error: {e}")