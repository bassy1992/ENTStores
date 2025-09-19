#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

# Test admin login via Django test client
try:
    print("=== ADMIN LOGIN TEST ===")
    
    # Create test client
    client = Client()
    
    # Get admin login page
    login_url = '/admin/login/'
    response = client.get(login_url)
    print(f"✅ Admin login page status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Admin login page loads successfully")
        
        # Try to login
        login_data = {
            'username': 'admin',
            'password': 'password123',
            'next': '/admin/'
        }
        
        # Get CSRF token from the form
        csrf_token = None
        if hasattr(response, 'context') and response.context:
            csrf_token = response.context.get('csrf_token')
        
        if csrf_token:
            login_data['csrfmiddlewaretoken'] = csrf_token
            print(f"✅ CSRF token found: {str(csrf_token)[:20]}...")
        else:
            print("⚠️ No CSRF token found")
            
        # Attempt login
        login_response = client.post(login_url, login_data, follow=True)
        print(f"✅ Login attempt status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            # Check if we're redirected to admin dashboard
            if '/admin/' in login_response.request['PATH_INFO']:
                print("✅ Login successful - redirected to admin dashboard")
            else:
                print("❌ Login failed - still on login page")
                print(f"Current URL: {login_response.request['PATH_INFO']}")
        else:
            print(f"❌ Login failed with status: {login_response.status_code}")
            
    else:
        print(f"❌ Admin login page failed to load: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()