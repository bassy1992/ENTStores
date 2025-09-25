#!/usr/bin/env python
"""
Test specific product reviews
"""
import requests
import json

def test_specific_reviews():
    """Test reviews for specific products"""
    
    base_url = "https://entstores.onrender.com"
    
    print("🧪 Testing specific product reviews...")
    
    # Get all products first
    print("\n1️⃣ Getting all products...")
    try:
        response = requests.get(f"{base_url}/api/shop/products/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            products = data.get('results', [])
            print(f"   ✅ Found {len(products)} products")
            
            # Look for products that should have reviews
            target_products = []
            for product in products:
                title = product.get('title', '').lower()
                if 'fghfhghgh' in title or 'faster than light' in title:
                    target_products.append(product)
                    print(f"   🎯 Target product: {product.get('id')} - {product.get('title')}")
            
            # Test reviews for each target product
            for product in target_products:
                product_id = product.get('id')
                print(f"\n2️⃣ Testing reviews for {product_id}...")
                
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
                        for review in reviews:
                            print(f"      📝 {review.get('user_name')}: {review.get('title')} ({review.get('rating')}★)")
                    else:
                        print("   ⚠️ No reviews found for this product")
                else:
                    print(f"   ❌ API failed: {reviews_response.text}")
            
            if not target_products:
                print("   ⚠️ No target products found. Checking first few products...")
                for product in products[:3]:
                    product_id = product.get('id')
                    print(f"\n🔍 Checking {product_id} - {product.get('title')[:50]}...")
                    
                    reviews_url = f"{base_url}/api/shop/products/{product_id}/reviews/"
                    reviews_response = requests.get(reviews_url, timeout=10)
                    
                    if reviews_response.status_code == 200:
                        reviews_data = reviews_response.json()
                        reviews = reviews_data.get('reviews', [])
                        print(f"      Reviews: {len(reviews)}")
                        
                        if reviews:
                            print(f"      🎉 FOUND REVIEWS! Product {product_id} has {len(reviews)} reviews")
                            break
        else:
            print(f"   ❌ Products API failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == '__main__':
    test_specific_reviews()