#!/usr/bin/env python
"""
Test production API endpoints
"""
import requests
import json

def test_production_api():
    """Test the production API endpoints"""
    
    base_url = "https://entstores.onrender.com"
    
    print("🧪 Testing production API endpoints...")
    
    # Test 1: Get products
    print("\n1️⃣ Testing products endpoint...")
    try:
        response = requests.get(f"{base_url}/api/shop/products/", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('results', [])
            print(f"   ✅ Found {len(products)} products")
            
            if products:
                first_product = products[0]
                product_id = first_product.get('id')
                print(f"   📦 First product: {product_id} - {first_product.get('title')}")
                
                # Test 2: Get reviews for first product
                print(f"\n2️⃣ Testing reviews for product {product_id}...")
                try:
                    reviews_url = f"{base_url}/api/shop/products/{product_id}/reviews/"
                    reviews_response = requests.get(reviews_url, timeout=10)
                    print(f"   URL: {reviews_url}")
                    print(f"   Status: {reviews_response.status_code}")
                    
                    if reviews_response.status_code == 200:
                        reviews_data = reviews_response.json()
                        reviews = reviews_data.get('reviews', [])
                        stats = reviews_data.get('stats', {})
                        
                        print(f"   ✅ Found {len(reviews)} reviews")
                        print(f"   📊 Stats: avg={stats.get('average_rating', 0)}, total={stats.get('total_reviews', 0)}")
                        
                        if reviews:
                            first_review = reviews[0]
                            print(f"   📝 First review: {first_review.get('user_name')} - {first_review.get('title')}")
                        else:
                            print("   ⚠️ No reviews found - this is the issue!")
                    else:
                        print(f"   ❌ Reviews API failed: {reviews_response.text}")
                        
                except Exception as e:
                    print(f"   ❌ Reviews API error: {e}")
            else:
                print("   ⚠️ No products found")
        else:
            print(f"   ❌ Products API failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Products API error: {e}")
    
    # Test 3: Test admin access
    print("\n3️⃣ Testing admin access...")
    try:
        admin_response = requests.get(f"{base_url}/admin/", timeout=10)
        print(f"   Status: {admin_response.status_code}")
        
        if admin_response.status_code == 200:
            print("   ✅ Admin is accessible")
        else:
            print(f"   ⚠️ Admin response: {admin_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Admin error: {e}")
    
    print("\n🏁 Production API test completed!")
    print("\n📋 If reviews are missing:")
    print("   1. SSH into Render and run: python manage.py setup_reviews")
    print("   2. Or run the migration script on the server")
    print("   3. Check Django admin for review tables")

if __name__ == '__main__':
    test_production_api()