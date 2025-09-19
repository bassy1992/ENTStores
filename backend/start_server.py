#!/usr/bin/env python
"""
Start the Django development server with proper CORS settings
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    
    print("🚀 Starting ENNC Shop API Server...")
    print("📡 API will be available at: http://localhost:8000/api/shop/")
    print("🔧 Admin panel at: http://localhost:8000/admin/ (admin/admin123)")
    print("🌐 CORS enabled for frontend at: http://localhost:8080")
    print("=" * 60)
    
    try:
        execute_from_command_line(['manage.py', 'runserver', '8000'])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
        sys.exit(0)