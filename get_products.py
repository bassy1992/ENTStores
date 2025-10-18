#!/usr/bin/env python3
"""
Get available products from API
"""

import requests
import json

def get_products():
    """Get products from API"""
    try:
        response = requests.get("https://entstores-production.up.railway.app/api/shop/products/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            products = data.get('results', [])
            
            print(f"Found {len(products)} products:")
            for product in products[:3]:  # Show first 3 products
                print(f"- ID: {product['id']}")
                print(f"  Title: {product['title']}")
                print(f"  Price: {product['price']}")
                print(f"  Shipping: {product.get('shipping_cost', 'Not set')}")
                print()
            
            return products[0] if products else None
        else:
            print(f"Failed to get products: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting products: {e}")
        return None

if __name__ == "__main__":
    product = get_products()
    if product:
        print(f"First product ID for testing: {product['id']}")
    else:
        print("No products available")