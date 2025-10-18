#!/usr/bin/env python3
"""
Test shipping integration after deployment
"""

import requests
import time

def test_shipping_integration():
    """Test the shipping integration"""
    
    print("🧪 Testing shipping integration...")
    
    # Wait for service to be ready
    print("⏳ Waiting for service to be ready...")
    for i in range(6):  # Try for 3 minutes
        try:
            response = requests.get("https://entstores-production.up.railway.app/api/health/", timeout=10)
            if response.status_code == 200:
                print("✅ Service is ready!")
                break
        except:
            pass
        
        if i < 5:
            print(f"   Attempt {i+1}/6 - waiting 30 seconds...")
            time.sleep(30)
    
    # Test products API
    try:
        print("\n📦 Testing products API...")
        response = requests.get("https://entstores-production.up.railway.app/api/shop/products/", timeout=30)
        
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Products API working - found {len(products)} products")
            
            if products and len(products) > 0:
                first_product = products[0]
                if 'shipping_cost' in first_product:
                    print(f"✅ Shipping cost field present: ${first_product['shipping_cost']}")
                    
                    # Show sample product with shipping
                    print(f"\n📋 Sample Product:")
                    print(f"   Name: {first_product.get('title', 'Unknown')}")
                    print(f"   Price: ${first_product.get('price', 0)}")
                