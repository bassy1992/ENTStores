#!/usr/bin/env python3
"""
Script to fix category issues and add missing categories.
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Category, Product

def fix_categories():
    """Add missing categories and fix any issues."""
    
    categories = [
        {'key': 't-shirts', 'label': 'T-Shirts', 'description': 'Premium cotton t-shirts'},
        {'key': 'polos', 'label': 'Polos', 'description': 'Classic polo shirts'},
        {'key': 'hoodies', 'label': 'Hoodies', 'description': 'Comfortable hoodies'},
        {'key': 'jeans', 'label': 'Jeans', 'description': 'Denim jeans'},
        {'key': 'accessories', 'label': 'Accessories', 'description': 'Fashion accessories'},
        {'key': 'shoes', 'label': 'Shoes', 'description': 'Footwear collection'},
    ]
    
    print("Adding/updating categories...")
    for cat in categories:
        category, created = Category.objects.get_or_create(
            key=cat['key'],
            defaults={
                'label': cat['label'], 
                'description': cat['description'],
                'featured': cat['key'] in ['t-shirts', 'hoodies']
            }
        )
        if created:
            print(f"✅ Created category: {cat['label']}")
        else:
            # Update existing category
            category.label = cat['label']
            category.description = cat['description']
            category.save()
            print(f"🔄 Updated category: {cat['label']}")
    
    print(f"\nTotal categories: {Category.objects.count()}")
    
    # Check products
    print(f"Total products: {Product.objects.count()}")
    for product in Product.objects.all():
        print(f"Product: {product.title} -> Category: {product.category.label}")

if __name__ == '__main__':
    fix_categories()