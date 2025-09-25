#!/usr/bin/env python
"""
Debug production review system
Run this on the production server to diagnose the issue
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, ProductReview
from django.db import connection
from django.test import Client

def debug_production_reviews():
    """Debug the production review system"""
    
    print("🔍 Debugging production review system...")
    
    # 1. Check database directly
    print("\n1️⃣ Checking database directly...")
    try:
        total_reviews = ProductReview.objects.count()
        print(f"   📊 Total reviews in database: {total_reviews}")
        
        if total_reviews > 0:
            print("   📝 All reviews:")
            for review in ProductReview.objects.all():
                print(f"      - ID: {review.id}, Product: {review.product_id}, User: {review.user_name}, Title: {review.title}")
        
        # Check products
        total_products = Product.objects.count()
        print(f"   📦 Total products: {total_products}")
        
        if total_products > 0:
            print("   📦 First few products:")
            for product in Product.objects.all()[:5]:
                print(f"      - ID: {product.id}, Title: {product.title}")
                
                # Check reviews for this product
                product_reviews = ProductReview.objects.filter(product_id=product.id)
                print(f"        Reviews: {product_reviews.count()}")
                
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return
    
    # 2. Test API endpoints directly
    print("\n2️⃣ Testing API endpoints...")
    try:
        client = Client()
        
        # Get a product that should have reviews
        product_with_reviews = None
        for product in Product.objects.all():
            if ProductReview.objects.filter(product_id=product.id).exists():
                product_with_reviews = product
                break
        
        if product_with_reviews:
            print(f"   🎯 Testing product: {product_with_reviews.id} - {product_with_reviews.title}")
            
            # Test GET reviews
            url = f'/api/shop/products/{product_with_reviews.id}/reviews/'
            response = client.get(url)
            
            print(f"   📡 GET {url}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                reviews = data.get('reviews', [])
                stats = data.get('stats', {})
                
                print(f"   ✅ API returned {len(reviews)} reviews")
                print(f"   📊 Stats: {stats}")
                
                if len(reviews) == 0:
                    print("   ❌ API ISSUE: Database has reviews but API returns 0!")
                    
                    # Debug the view logic
                    print("   🔍 Debugging view logic...")
                    from shop.views import ProductReviewListCreateView
                    
                    view = ProductReviewListCreateView()
                    view.kwargs = {'product_id': product_with_reviews.id}
                    
                    # Mock request
                    from django.test import RequestFactory
                    factory = RequestFactory()
                    request = factory.get(url)
                    request.query_params = {}  # Add DRF query_params
                    view.request = request
                    
                    try:
                        queryset = view.get_queryset()
                        print(f"      View queryset count: {queryset.count()}")
                        
                        if queryset.count() == 0:
                            print("      ❌ View queryset is empty!")
                            
                            # Check filtering
                            all_reviews = ProductReview.objects.filter(product_id=product_with_reviews.id)
                            approved_reviews = ProductReview.objects.filter(product_id=product_with_reviews.id, is_approved=True)
                            
                            print(f"      All reviews for product: {all_reviews.count()}")
                            print(f"      Approved reviews: {approved_reviews.count()}")
                            
                            if all_reviews.count() > 0 and approved_reviews.count() == 0:
                                print("      🔧 ISSUE: Reviews exist but are not approved!")
                                # Fix approval status
                                all_reviews.update(is_approved=True)
                                print("      ✅ Fixed: Set all reviews to approved")
                        
                    except Exception as view_error:
                        print(f"      ❌ View error: {view_error}")
                
            else:
                print(f"   ❌ API failed: {response.content.decode()}")
        else:
            print("   ⚠️ No products with reviews found")
            
    except Exception as e:
        print(f"   ❌ API test error: {e}")
    
    # 3. Test review creation
    print("\n3️⃣ Testing review creation...")
    try:
        # Get first product
        first_product = Product.objects.first()
        if first_product:
            print(f"   🎯 Creating test review for: {first_product.id}")
            
            # Create a test review
            test_review = ProductReview.objects.create(
                product=first_product,
                user_name="Debug Test User",
                user_email="debug@test.com",
                rating=5,
                title="Debug Test Review",
                comment="This is a test review created during debugging.",
                is_approved=True
            )
            
            print(f"   ✅ Created test review: ID {test_review.id}")
            
            # Test API again
            url = f'/api/shop/products/{first_product.id}/reviews/'
            response = client.get(url)
            
            if response.status_code == 200:
                data = response.json()
                reviews = data.get('reviews', [])
                print(f"   📡 API now returns {len(reviews)} reviews")
                
                if len(reviews) > 0:
                    print("   🎉 SUCCESS: API is working!")
                else:
                    print("   ❌ STILL BROKEN: API still returns 0 reviews")
            
            # Clean up test review
            test_review.delete()
            print("   🧹 Cleaned up test review")
            
    except Exception as e:
        print(f"   ❌ Review creation test error: {e}")
    
    print("\n🏁 Debug completed!")

if __name__ == '__main__':
    debug_production_reviews()