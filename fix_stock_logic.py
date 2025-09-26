#!/usr/bin/env python
"""
Script to fix the stock logic issue where products with variants 
show as out of stock even when variants have stock.
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

def test_stock_logic():
    """Test the updated stock logic"""
    print("Testing updated stock logic...")
    
    # Get all products
    products = Product.objects.all()
    print(f"Total products: {products.count()}")
    
    for product in products:
        # Get variant stock info
        variant_stock = 0
        try:
            variants = product.variants.filter(is_available=True)
            variant_stock = sum(v.stock_quantity for v in variants)
        except Exception as e:
            print(f"Error getting variants for {product.title}: {e}")
        
        print(f"\nProduct: {product.title}")
        print(f"  Main stock: {product.stock_quantity}")
        print(f"  Variant stock: {variant_stock}")
        print(f"  Is in stock (old logic): {product.stock_quantity > 0}")
        print(f"  Is in stock (new logic): {product.is_in_stock}")

if __name__ == "__main__":
    test_stock_logic()