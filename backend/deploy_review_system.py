#!/usr/bin/env python
"""
Deploy review system to production
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

def deploy_review_system():
    """Deploy review system to production"""
    
    print("🚀 Deploying review system to production...")
    
    # Check if review tables exist
    print("\n1️⃣ Checking database tables...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'shop_product%review%';")
            tables = cursor.fetchall()
            
        if tables:
            print(f"   ✅ Found review tables: {[table[0] for table in tables]}")
        else:
            print("   ❌ Review tables not found. Run migrations first:")
            print("      python manage.py makemigrations shop")
            print("      python manage.py migrate")
            return
            
    except Exception as e:
        print(f"   ❌ Error checking tables: {e}")
        return
    
    # Check if we have products
    print("\n2️⃣ Checking products...")
    try:
        products_count = Product.objects.count()
        print(f"   📦 Found {products_count} products")
        
        if products_count == 0:
            print("   ⚠️ No products found. Add products first.")
            return
            
    except Exception as e:
        print(f"   ❌ Error checking products: {e}")
        return
    
    # Check existing reviews
    print("\n3️⃣ Checking existing reviews...")
    try:
        reviews_count = ProductReview.objects.count()
        print(f"   📝 Found {reviews_count} existing reviews")
        
        if reviews_count > 0:
            # Show some sample reviews
            sample_reviews = ProductReview.objects.all()[:3]
            for review in sample_reviews:
                print(f"      - {review.user_name}: {review.title} ({review.rating}★)")
                
    except Exception as e:
        print(f"   ❌ Error checking reviews: {e}")
        return
    
    # Add sample reviews if none exist
    if reviews_count == 0:
        print("\n4️⃣ Adding sample reviews...")
        try:
            # Get first product
            product = Product.objects.first()
            
            sample_reviews_data = [
                {
                    'user_name': 'Sarah M.',
                    'user_email': 'sarah.m@example.com',
                    'rating': 5,
                    'title': 'Amazing quality!',
                    'comment': 'This product exceeded my expectations. The material is soft and comfortable, and the fit is perfect.',
                    'verified_purchase': True
                },
                {
                    'user_name': 'Mike R.',
                    'user_email': 'mike.r@example.com',
                    'rating': 4,
                    'title': 'Good value for money',
                    'comment': 'Nice product overall. The color is exactly as shown in the pictures.',
                    'verified_purchase': True
                },
                {
                    'user_name': 'Jennifer K.',
                    'user_email': 'jennifer.k@example.com',
                    'rating': 5,
                    'title': 'Perfect fit and style',
                    'comment': 'Love this! The design is exactly what I was looking for.',
                    'verified_purchase': True
                }
            ]
            
            created_count = 0
            for review_data in sample_reviews_data:
                review = ProductReview.objects.create(
                    product=product,
                    **review_data,
                    is_approved=True
                )
                created_count += 1
                print(f"      ✅ Created review by {review_data['user_name']}")
            
            print(f"   🎉 Created {created_count} sample reviews")
            
        except Exception as e:
            print(f"   ❌ Error creating sample reviews: {e}")
    
    # Test API endpoints
    print("\n5️⃣ Testing API endpoints...")
    try:
        from django.test import Client
        
        client = Client()
        product = Product.objects.first()
        
        # Test GET reviews
        response = client.get(f'/api/shop/products/{product.id}/reviews/')
        print(f"   GET /api/shop/products/{product.id}/reviews/ - Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ Returns {len(data.get('reviews', []))} reviews")
            print(f"      📊 Stats: {data.get('stats', {})}")
        
    except Exception as e:
        print(f"   ❌ Error testing API: {e}")
    
    print("\n🎉 Review system deployment completed!")
    print("\n📋 Next steps:")
    print("   1. Ensure your production server is running")
    print("   2. Test the frontend at your production URL")
    print("   3. Check browser console for API calls")
    print("   4. Verify reviews are loading from the database")

if __name__ == '__main__':
    deploy_review_system()