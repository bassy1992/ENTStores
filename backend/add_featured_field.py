#!/usr/bin/env python3
"""
Script to add is_featured field to Product model and create migration
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('/workspaces/entstores/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.core.management import execute_from_command_line

def main():
    print("Creating migration for is_featured field...")
    
    # Create migration
    execute_from_command_line(['manage.py', 'makemigrations', 'shop'])
    
    print("Migration created successfully!")
    print("Now applying migration...")
    
    # Apply migration
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("Migration applied successfully!")
    
    # Set some products as featured
    from shop.models import Product
    
    print("Setting some products as featured...")
    
    # Get first 4 products and mark them as featured
    products = Product.objects.all()[:4]
    for product in products:
        product.is_featured = True
        product.save()
        print(f"✓ Set {product.title} as featured")
    
    print(f"Successfully set {len(products)} products as featured!")

if __name__ == '__main__':
    main()