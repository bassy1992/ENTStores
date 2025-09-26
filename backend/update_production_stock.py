#!/usr/bin/env python3
"""
Script to update stock quantities for products in production database.
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set production database URL
os.environ['DATABASE_URL'] = 'postgresql://entstore_db_user:m3we2cxnqRNZSMc6B5RK0vDsnku7QAXa@dpg-d36utrmmcj7s73e0q0dg-a/entstore_db'
os.environ['USE_SQLITE'] = 'false'

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product

def update_product_stock():
    """Update stock for existing products."""
    print("Updating product stock in production database...")
    
    # Get all products
    products = Product.objects.all()
    
    for product in products:
        # Update stock to a reasonable amount
        old_stock = product.stock_quantity
        product.stock_quantity = 25  # Set to 25 items in stock
        product.save()
        
        print(f"✅ Updated {product.title}: {old_stock} → {product.stock_quantity} (In stock: {product.is_in_stock})")
    
    print(f"\n✅ Updated stock for {products.count()} products!")

if __name__ == '__main__':
    update_product_stock()