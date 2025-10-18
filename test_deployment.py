#!/usr/bin/env python
import requests
import json
import time

def test_deployment():
    """Test if the stock fix has been deployed to production"""
    print("🧪 Testing deployment of stock fix...")
    
    # Wait a moment for deployment to complete
    print("⏳ Waiting for deployment to complete...")
    time.sleep(10)
    
    # Test the production API
    production_url = "https://entstores-production.up.railway.app/api/shop/products/shorts-coral-pink/"
    
    try:
        print(f"📡 Testing: {production_url}")
        response = requests.get(production_url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n📦 Product: {data.get('title', 'N/A')}")
            print(f"📊 Main Stock: {data.get('stock_quantity', 'N/A')}")
            print(f"✅ Is In Stock: {data.get('is_in_stock', 'N/A')}")
            
            # Check variants
            variants = data.get('variants', [])
            variant_stock = sum(v.get('stock_quantity', 0) for v in variants if v.get('is_available', False))
            print(f"🎯 Variant Stock: {variant_stock}")
            
            # Test result
            if data.get('is_in_stock') == True and variant_stock > 0:
                print("\n🎉 SUCCESS! Stock fix has been deployed successfully!")
                print("✅ Product now shows as 'In Stock' despite main stock being 0")
                print("✅ Variant stock is properly considered")
                return True
            elif data.get('is_in_stock') == False and variant_stock > 0:
                print("\n⚠️  DEPLOYMENT PENDING: Stock fix not yet active")
                print("❌ Product still shows as 'Out of Stock'")
                print("🔄 This may take a few more minutes to deploy")
                return False
            else:
                print("\n❓ UNEXPECTED: Check the data manually")
                return False
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to production API: {e}")
        return False

def test_shop_page():
    """Test the shop page API to see if products show correct stock status"""
    print("\n🛍️  Testing shop page API...")
    
    try:
        list_url = "https://entstores-production.up.railway.app/api/shop/products/"
        response = requests.get(list_url)
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('results', [])
            
            # Look for shorts products
            shorts_products = [p for p in products if 'shorts' in p.get('title', '').lower()]
            print(f"Found {len(shorts_products)} shorts products:")
            
            for product in shorts_products:
                title = product.get('title', 'N/A')
                stock = product.get('stock_quantity', 'N/A')
                in_stock = product.get('is_in_stock', 'N/A')
                print(f"  - {title}: stock={stock}, in_stock={in_stock}")
                
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing stock fix deployment...")
    print("=" * 50)
    
    # Test the specific product
    success = test_deployment()
    
    # Test the shop page
    test_shop_page()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Deployment successful! The stock issue has been fixed.")
        print("🌐 Visit: https://www.enontinoclothingstore.com/product/shorts-coral-pink")
        print("✅ The product should now show as 'In Stock' on the shop page")
    else:
        print("⏳ Deployment may still be in progress...")
        print("🔄 Try running this test again in a few minutes")
        print("📝 Or check your deployment platform for status updates")