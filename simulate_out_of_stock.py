#!/usr/bin/env python3
"""
Simulate out of stock scenario for testing
"""

import os
import sys
import django

# Setup Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product

def simulate_out_of_stock():
    """Set a product to out of stock for testing"""
    print("🧪 Simulating Out of Stock Scenario")
    print("=" * 50)
    
    # Get the first product
    product = Product.objects.first()
    if not product:
        print("❌ No products found")
        return
    
    print(f"📦 Selected product: {product.title}")
    print(f"   Current stock: {product.stock_quantity}")
    print(f"   Currently in stock: {product.is_in_stock}")
    
    # Set stock to 0
    original_stock = product.stock_quantity
    product.stock_quantity = 0
    product.save()
    
    print(f"\n🔄 Updated stock to 0")
    print(f"   New stock: {product.stock_quantity}")
    print(f"   Now in stock: {product.is_in_stock}")
    
    print(f"\n✅ Product '{product.title}' is now out of stock")
    print(f"   Product ID: {product.id}")
    print(f"   You can now test the stock validation with this product")
    
    print(f"\n🔧 To restore stock later, run:")
    print(f"   python -c \"")
    print(f"import os, sys, django")
    print(f"sys.path.append('backend')")
    print(f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')")
    print(f"django.setup()")
    print(f"from shop.models import Product")
    print(f"p = Product.objects.get(id='{product.id}')")
    print(f"p.stock_quantity = {original_stock}")
    print(f"p.save()")
    print(f"print('Stock restored')\"")

if __name__ == "__main__":
    simulate_out_of_stock()