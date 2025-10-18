#!/usr/bin/env python3
"""
⚠️ DEPRECATED: Startup script for Render deployment (now using Railway)
This ensures we're in the right directory and using the correct WSGI application
"""
import os
import sys
import subprocess

# Change to backend directory
os.chdir('backend')

# Add backend to Python path
sys.path.insert(0, os.getcwd())

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Get port from environment
port = os.environ.get('PORT', '8000')

# Start gunicorn
cmd = [
    'gunicorn',
    'myproject.wsgi:application',
    '--host', '0.0.0.0',
    '--port', port,
    '--workers', '2',
    '--timeout', '120'
]

print(f"Starting Django app with command: {' '.join(cmd)}")
subprocess.run(cmd)