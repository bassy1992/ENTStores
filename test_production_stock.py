#!/usr/bin/env python
import requests
import json

# Test the production API
production_url = "https://entstores.onrender.com/api/shop/products/shorts-coral-pink/"

try:
    print("Testing production API...")
    response = requests.get(production_url)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nProduct: {data.get('title', 'N/A')}")
        print(f"Stock Quantity: {data.get('stock_quantity', 'N/A')}")
        print(f"Is In Stock: {data.get('is_in_stock', 'N/A')}")
        print(f"Is Active: {data.get('is_active', 'N/A')}")
        
        # Check if there are variants
        variants = data.get('variants', [])
        print(f"\nVariants: {len(variants)}")
        for variant in variants:
            print(f"- Size: {variant.get('size', {}).get('name', 'N/A')}, Color: {variant.get('color', {}).get('name', 'N/A')}, Stock: {variant.get('stock_quantity', 'N/A')}, In Stock: {variant.get('is_in_stock', 'N/A')}")
        
        print(f"\nFull response:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"Error connecting to production API: {e}")

# Also test the products list endpoint
try:
    print("\n" + "="*50)
    print("Testing products list API...")
    list_url = "https://entstores.onrender.com/api/shop/products/"
    response = requests.get(list_url)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        products = data.get('results', [])
        print(f"Total products: {len(products)}")
        
        # Look for shorts products
        shorts_products = [p for p in products if 'shorts' in p.get('title', '').lower()]
        print(f"Shorts products: {len(shorts_products)}")
        
        for product in shorts_products:
            print(f"- {product.get('title', 'N/A')} (stock: {product.get('stock_quantity', 'N/A')}, in_stock: {product.get('is_in_stock', 'N/A')})")
            
except Exception as e:
    print(f"Error connecting to production list API: {e}")