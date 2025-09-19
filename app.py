"""
WSGI application entry point for Render deployment
This file redirects to the Django WSGI application
"""
import os
import sys

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Import Django WSGI application
from myproject.wsgi import application

# Export for gunicorn
app = application