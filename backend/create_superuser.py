#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
try:
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_superuser(
            username='admin',
            email='admin@enintino.com',
            password='SecurePass2024!'
        )
        print(f"✅ Created superuser: {user.username}")
    else:
        print("✅ Superuser already exists")
        # Reset password just in case
        user = User.objects.get(username='admin')
        user.set_password('SecurePass2024!')
        user.save()
        print("✅ Password reset for existing superuser")
        
except Exception as e:
    print(f"❌ Error: {e}")