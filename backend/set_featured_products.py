#!/usr/bin/env python3
"""
Script to set some products as featured for testing
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('/workspaces/entstores/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product

def main():
    print("Setting products as featured...")
    
    # Get all products
    products = Product.objects.all()
    
    if not products.exists():
        print("No products found in database!")
        return
    
    print(f"Found {products.count()} products in database")
    
    # Set first 6 products as featured
    featured_products = products[:6]
    
    for product in featured_products:
        product.is_featured = True
        product.save()
        print(f"✓ Set '{product.title}' as featured")
    
    # Ensure other products are not featured
    non_featured = products[6:]
    for product in non_featured:
        if product.is_featured:
            product.is_featured = False
            product.save()
            print(f"✗ Removed featured status from '{product.title}'")
    
    print(f"\nSuccessfully set {len(featured_products)} products as featured!")
    
    # Show current featured products
    featured = Product.objects.filter(is_featured=True)
    print(f"\nCurrent featured products ({featured.count()}):")
    for product in featured:
        print(f"  - {product.title} (ID: {product.id})")

if __name__ == '__main__':
    main()