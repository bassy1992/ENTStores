#!/usr/bin/env python
"""
Test the review API endpoints
"""
import os
import sys
import django
import requests
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, ProductReview

def test_review_api():
    """Test the review API endpoints"""
    
    # Get a product with reviews
    product = Product.objects.first()
    if not product:
        print("❌ No products found")
        return
    
    print(f"🧪 Testing review API for product: {product.title} (ID: {product.id})")
    
    # Test 1: Get reviews
    print("\n1️⃣ Testing GET reviews endpoint...")
    try:
        url = f"http://127.0.0.1:8000/api/shop/products/{product.id}/reviews/"
        print(f"   URL: {url}")
        
        response = requests.get(url, timeout=5)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Found {len(data.get('reviews', []))} reviews")
            print(f"   📊 Stats: {data.get('stats', {})}")
            
            # Show first review
            if data.get('reviews'):
                first_review = data['reviews'][0]
                print(f"   📝 First review: {first_review.get('user_name')} - {first_review.get('title')}")
        else:
            print(f"   ❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Create a new review
    print("\n2️⃣ Testing POST review endpoint...")
    try:
        url = f"http://127.0.0.1:8000/api/shop/products/{product.id}/reviews/"
        
        review_data = {
            "user_name": "Test User",
            "user_email": "test@example.com",
            "rating": 5,
            "title": "Test Review",
            "comment": "This is a test review to check if the API is working properly.",
            "size_purchased": "M",
            "color_purchased": "Blue"
        }
        
        print(f"   URL: {url}")
        print(f"   Data: {json.dumps(review_data, indent=2)}")
        
        response = requests.post(
            url, 
            json=review_data,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"   ✅ Success! Review created: {data}")
        else:
            print(f"   ❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Check database directly
    print("\n3️⃣ Checking database directly...")
    try:
        total_reviews = ProductReview.objects.filter(product=product).count()
        print(f"   📊 Total reviews in database for this product: {total_reviews}")
        
        if total_reviews > 0:
            latest_review = ProductReview.objects.filter(product=product).order_by('-created_at').first()
            print(f"   📝 Latest review: {latest_review.user_name} - {latest_review.title} ({latest_review.rating}★)")
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
    
    print("\n🏁 Test completed!")

if __name__ == '__main__':
    test_review_api()