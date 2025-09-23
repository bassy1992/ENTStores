#!/usr/bin/env python3
"""
Script to add sample featured products with proper data
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('/workspaces/entstores/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, Category

def main():
    print("Adding sample featured products...")
    
    # Get or create categories
    try:
        tshirt_category = Category.objects.get(key='t-shirts')
    except Category.DoesNotExist:
        tshirt_category = Category.objects.create(
            key='t-shirts',
            label='T-Shirts',
            description='Premium cotton t-shirts'
        )
    
    try:
        hoodie_category = Category.objects.get(key='hoodies')
    except Category.DoesNotExist:
        hoodie_category = Category.objects.create(
            key='hoodies',
            label='Hoodies',
            description='Comfortable hoodies and sweatshirts'
        )
    
    # Sample products data
    sample_products = [
        {
            'id': 'ennc-classic-tee-black',
            'title': 'ENNC Classic Tee — Black',
            'slug': 'ennc-classic-tee-black',
            'price': 2800,  # $28.00
            'description': 'Premium cotton t-shirt with signature ENNC logo. Comfortable fit and durable construction.',
            'category': tshirt_category,
            'stock_quantity': 50,
            'is_featured': True,
        },
        {
            'id': 'ennc-classic-tee-white',
            'title': 'ENNC Classic Tee — White',
            'slug': 'ennc-classic-tee-white',
            'price': 2800,  # $28.00
            'description': 'Clean white t-shirt with minimalist ENNC branding. Perfect for everyday wear.',
            'category': tshirt_category,
            'stock_quantity': 45,
            'is_featured': True,
        },
        {
            'id': 'ennc-essential-hoodie-grey',
            'title': 'ENNC Essential Hoodie — Grey',
            'slug': 'ennc-essential-hoodie-grey',
            'price': 6500,  # $65.00
            'description': 'Heavyweight cotton hoodie with kangaroo pocket and adjustable drawstring hood.',
            'category': hoodie_category,
            'stock_quantity': 30,
            'is_featured': True,
        },
        {
            'id': 'ennc-essential-hoodie-black',
            'title': 'ENNC Essential Hoodie — Black',
            'slug': 'ennc-essential-hoodie-black',
            'price': 6500,  # $65.00
            'description': 'Classic black hoodie with premium fleece lining and embroidered logo.',
            'category': hoodie_category,
            'stock_quantity': 35,
            'is_featured': True,
        },
    ]
    
    created_count = 0
    updated_count = 0
    
    for product_data in sample_products:
        product, created = Product.objects.get_or_create(
            id=product_data['id'],
            defaults=product_data
        )
        
        if created:
            created_count += 1
            print(f"✓ Created new product: {product.title}")
        else:
            # Update existing product to be featured
            product.is_featured = True
            product.save()
            updated_count += 1
            print(f"✓ Updated existing product: {product.title}")
    
    print(f"\nSummary:")
    print(f"  - Created: {created_count} new products")
    print(f"  - Updated: {updated_count} existing products")
    
    # Show all featured products
    featured = Product.objects.filter(is_featured=True)
    print(f"\nAll featured products ({featured.count()}):")
    for product in featured:
        print(f"  - {product.title} - {product.price_display}")

if __name__ == '__main__':
    main()