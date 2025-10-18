#!/usr/bin/env python3
"""
Production Database Shell
Direct access to production PostgreSQL database
"""

import os
import sys
import django

# Setup
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
os.environ.setdefault('RAILWAY_ENVIRONMENT', 'production')

django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    print("Opening production database shell...")
    print("Type \\q to quit")
    call_command('dbshell')