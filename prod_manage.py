#!/usr/bin/env python3
"""
Production Django Management Script
Run Django commands against production database
"""

import os
import sys
import django

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
os.environ.setdefault('RAILWAY_ENVIRONMENT', 'production')

# Setup Django
django.setup()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    
    # Add 'manage.py' as first argument if not present
    if len(sys.argv) == 1 or sys.argv[1] != 'manage.py':
        sys.argv.insert(1, 'manage.py')
    
    execute_from_command_line(sys.argv[1:])