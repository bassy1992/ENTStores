#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

# Delete existing superusers
try:
    superusers = User.objects.filter(is_superuser=True)
    count = superusers.count()
    superusers.delete()
    print(f"✅ Deleted {count} existing superuser(s)")
    
    # Create new superuser with new credentials
    username = "admin"
    email = "admin@enintino.com"
    password = "SecurePass2024!"
    
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ Created new superuser: {user.username}")
    print(f"📧 Email: {user.email}")
    print(f"🔑 Password: {password}")
    
except Exception as e:
    print(f"❌ Error: {e}")