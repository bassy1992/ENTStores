#!/usr/bin/env python
"""
Script to migrate from SQLite to PostgreSQL on Railway
Run this after setting up PostgreSQL in Railway
"""
import os
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    django.setup()
    
    print("Running migrations for PostgreSQL...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Creating superuser (if needed)...")
    # You can uncomment this if you want to create a superuser automatically
    # execute_from_command_line(['manage.py', 'createsuperuser', '--noinput'])
    
    print("Migration to PostgreSQL complete!")