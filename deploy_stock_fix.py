#!/usr/bin/env python
"""
Deploy script to fix the stock logic issue in production.
This script will be run on the production server to update the code.
"""
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product

def fix_production_stock():
    """Fix stock display for products with variants"""
    print("Fixing production stock display...")
    
    # Find products that have 0 main stock but variants with stock
    problematic_products = []
    
    for product in Product.objects.all():
        if product.stock_quantity == 0:
            try:
                # Check if any variants have stock
                variants_with_stock = product.variants.filter(
                    stock_quantity__gt=0,
                    is_available=True
                ).count()
                
                if variants_with_stock > 0:
                    problematic_products.append({
                        'product': product,
                        'variants_with_stock': variants_with_stock
                    })
            except Exception as e:
                print(f"Error checking variants for {product.title}: {e}")
    
    print(f"Found {len(problematic_products)} products with stock issues:")
    
    for item in problematic_products:
        product = item['product']
        variants_count = item['variants_with_stock']
        
        print(f"\n- {product.title} (slug: {product.slug})")
        print(f"  Main stock: {product.stock_quantity}")
        print(f"  Variants with stock: {variants_count}")
        print(f"  Current is_in_stock: {product.is_in_stock}")
        
        # Show variant details
        try:
            variants = product.variants.filter(is_available=True)
            for variant in variants:
                print(f"    {variant.size.name} {variant.color.name}: {variant.stock_quantity} units")
        except Exception as e:
            print(f"    Error getting variant details: {e}")
    
    print(f"\nThe updated model logic will now correctly show these products as 'in stock'")
    print("because the is_in_stock property now checks both main stock and variant stock.")

if __name__ == "__main__":
    fix_production_stock()