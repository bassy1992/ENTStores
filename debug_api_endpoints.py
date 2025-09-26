#!/usr/bin/env python
import requests
import json

def test_different_endpoints():
    """Test different API endpoints to see which ones are updated"""
    
    print("🔍 Testing different API endpoints for stock status...")
    
    endpoints = [
        ("Product Detail", "https://entstores.onrender.com/api/shop/products/shorts-coral-pink/"),
        ("Products List", "https://entstores.onrender.com/api/shop/products/"),
        ("Simple Products", "https://entstores.onrender.com/api/shop/simple-products/"),
    ]
    
    for name, url in endpoints:
        print(f"\n📡 Testing {name}: {url}")
        try:
            response = requests.get(url)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if name == "Product Detail":
                    print(f"  Title: {data.get('title', 'N/A')}")
                    print(f"  Stock Quantity: {data.get('stock_quantity', 'N/A')}")
                    print(f"  Is In Stock: {data.get('is_in_stock', 'N/A')}")
                    print(f"  Variants: {len(data.get('variants', []))}")
                    
                else:  # List endpoints
                    results = data.get('results', [])
                    coral_pink = None
                    
                    for product in results:
                        if 'coral' in product.get('title', '').lower() and 'pink' in product.get('title', '').lower():
                            coral_pink = product
                            break
                    
                    if coral_pink:
                        print(f"  Found: {coral_pink.get('title', 'N/A')}")
                        print(f"  Stock Quantity: {coral_pink.get('stock_quantity', 'N/A')}")
                        print(f"  Is In Stock: {coral_pink.get('is_in_stock', 'N/A')}")
                    else:
                        print("  Coral Pink product not found in list")
            else:
                print(f"  Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"  Error: {e}")

def test_cache_busting():
    """Test with cache busting parameters"""
    print(f"\n🔄 Testing with cache busting...")
    
    import time
    timestamp = int(time.time())
    
    url = f"https://entstores.onrender.com/api/shop/products/?_t={timestamp}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            coral_pink = None
            for product in results:
                if 'coral' in product.get('title', '').lower() and 'pink' in product.get('title', '').lower():
                    coral_pink = product
                    break
            
            if coral_pink:
                print(f"  With cache busting - Is In Stock: {coral_pink.get('is_in_stock', 'N/A')}")
            else:
                print("  Product not found")
        else:
            print(f"  Error: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    test_different_endpoints()
    test_cache_busting()