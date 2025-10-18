#!/usr/bin/env python3
"""
Test script to verify shipping cost field is working
"""

import requests
import time

def test_shipping_field():
    """Test if the shipping cost field is available in the API"""
    
    print("🧪 Testing shipping cost field deployment...")
    
    # Wait a bit for deployment
    print("⏳ Waiting 30 seconds for deployment to complete...")
    time.sleep(30)
    
    # Test production API
    try:
        print("\n🌐 Testing production API...")
        response = requests.get("https://entstores-production.up.railway.app/api/shop/products/", timeout=30)
        
        if response.status_code == 200:
            products = response.json()
            print(f"✅ API responded successfully with {len(products)} products")
            
            if products and len(products) > 0:
                first_product = products[0]
                print(f"\n📦 First product: {first_product.get('title', 'Unknown')}")
                
                if 'shipping_cost' in first_product:
                    shipping_cost = first_product['shipping_cost']
                    print(f"✅ Shipping cost field found: ${shipping_cost}")
                    
                    # Show all fields for reference
                    print(f"\n📋 Available fields: {list(first_product.keys())}")
                    
                    return True
                else:
                    print("❌ Shipping cost field not found in API response")
                    print(f"Available fields: {list(first_product.keys())}")
                    return False
            else:
                print("⚠️ No products found in API response")
                return False
        else:
            print(f"❌ API returned status code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_admin_access():
    """Test if admin page is accessible"""
    try:
        print("\n🔐 Testing admin page access...")
        response = requests.get("https://entstores-production.up.railway.app/admin/shop/product/add/", timeout=30)
        
        if response.status_code in [200, 302]:  # 302 is redirect to login
            print("✅ Admin page is accessible")
            return True
        else:
            print(f"⚠️ Admin page returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing admin: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting shipping field verification...")
    
    api_success = test_shipping_field()
    admin_success = test_admin_access()
    
    if api_success:
        print("\n🎉 SUCCESS! Shipping cost field is working!")
        print("\n📋 Next steps:")
        print("1. Go to: https://entstores-production.up.railway.app/admin/shop/product/add/")
        print("2. Log in with your admin credentials")
        print("3. Look for 'Shipping cost' field in the 'Pricing & Category' section")
        print("4. Set shipping costs for your products (default is $9.99)")
        print("5. The shipping cost will appear in your cart calculations")
    else:
        print("\n⚠️ Shipping field may still be deploying. Try again in a few minutes.")
    
    if admin_success:
        print("\n✅ Admin interface is accessible")
    else:
        print("\n⚠️ Admin interface may need a few more minutes to deploy")