#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Category, Product
from django.contrib.auth.models import User

def reset_database():
    print("🗑️ Clearing existing data...")
    
    # Clear products and categories
    Product.objects.all().delete()
    Category.objects.all().delete()
    
    print("✅ Database cleared!")
    
    # Re-run seed data
    print("🌱 Re-seeding database...")
    exec(open('seed_data.py').read())

if __name__ == '__main__':
    reset_database()