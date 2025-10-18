#!/usr/bin/env python
"""
Railway startup script to create superuser and run migrations
"""
import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Change to backend directory
os.chdir('backend')

# Import Django and setup
import django
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    try:
        # Run migrations
        print("🔄 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Create superuser
        print("👤 Creating/updating superuser...")
        execute_from_command_line(['manage.py', 'create_admin'])
        
        print("✅ Railway startup complete!")
        
    except Exception as e:
        print(f"❌ Startup error: {e}")
        # Don't fail the deployment, just log the error
        pass