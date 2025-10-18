#!/usr/bin/env python3
"""
Production Django Shell
Interactive Python shell with production database access
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

# Import common models for convenience
from shop.models import *
from django.contrib.auth.models import User

if __name__ == '__main__':
    print("Opening production Django shell...")
    print("Available models: Product, Category, Order, OrderItem, etc.")
    print("Example: Product.objects.all()")
    
    from django.core.management import call_command
    call_command('shell')