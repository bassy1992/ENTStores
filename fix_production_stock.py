#!/usr/bin/env python3
"""
Script to fix stock quantities in production.
This script should be run on the production server or with production database access.
"""

import requests
import json

def update_stock_via_admin():
    """
    Instructions to update stock via Django admin:
    
    1. Go to https://entstores.onrender.com/admin/
    2. Login with admin credentials
    3. Go to Shop > Products
    4. Click on the product "gjgjkhjgjkhjg"
    5. Change the "Stock quantity" field from 0 to 25
    6. Click "Save"
    
    This will immediately update the stock and make the product show as "in stock"
    """
    print("To fix the stock issue:")
    print("1. Go to https://entstores.onrender.com/admin/")
    print("2. Login with admin credentials")
    print("3. Navigate to Shop > Products")
    print("4. Edit the product and set stock_quantity to 25")
    print("5. Save the changes")
    print("\nAlternatively, you can run this script on the production server:")
    print("python manage.py shell")
    print(">>> from shop.models import Product")
    print(">>> product = Product.objects.get(slug='gjgjkhjgjkhjg')")
    print(">>> product.stock_quantity = 25")
    print(">>> product.save()")
    print(">>> print(f'Updated {product.title}: Stock={product.stock_quantity}, In Stock={product.is_in_stock}')")

def test_api_after_fix():
    """Test the API to see if stock is updated"""
    try:
        response = requests.get("https://entstores.onrender.com/api/shop/products/")
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                product = data['results'][0]
                print(f"\nCurrent API Response:")
                print(f"Product: {product['title']}")
                print(f"Stock Quantity: {product['stock_quantity']}")
                print(f"Is In Stock: {product['is_in_stock']}")
                
                if product['is_in_stock']:
                    print("✅ Product is now showing as IN STOCK!")
                else:
                    print("❌ Product is still showing as OUT OF STOCK")
            else:
                print("No products found in API response")
        else:
            print(f"API request failed with status: {response.status_code}")
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == '__main__':
    print("=== Production Stock Fix ===")
    update_stock_via_admin()
    print("\n=== Testing Current API Status ===")
    test_api_after_fix()