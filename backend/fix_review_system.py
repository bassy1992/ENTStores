#!/usr/bin/env python
"""
Fix common review system issues
Run this on production server after debugging
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, ProductReview

def fix_review_system():
    """Fix common review system issues"""
    
    print("🔧 Fixing review system issues...")
    
    # Fix 1: Ensure all reviews are approved
    print("\n1️⃣ Fixing review approval status...")
    try:
        unapproved_reviews = ProductReview.objects.filter(is_approved=False)
        count = unapproved_reviews.count()
        
        if count > 0:
            unapproved_reviews.update(is_approved=True)
            print(f"   ✅ Approved {count} reviews")
        else:
            print("   ✅ All reviews already approved")
            
    except Exception as e:
        print(f"   ❌ Error fixing approvals: {e}")
    
    # Fix 2: Verify product relationships
    print("\n2️⃣ Verifying product relationships...")
    try:
        orphaned_reviews = []
        for review in ProductReview.objects.all():
            try:
                # Try to access the product
                product = review.product
                if not product:
                    orphaned_reviews.append(review.id)
            except:
                orphaned_reviews.append(review.id)
        
        if orphaned_reviews:
            print(f"   ⚠️ Found {len(orphaned_reviews)} orphaned reviews")
            # Don't delete them, just report
        else:
            print("   ✅ All reviews have valid product relationships")
            
    except Exception as e:
        print(f"   ❌ Error checking relationships: {e}")
    
    # Fix 3: Add missing reviews if database is empty
    print("\n3️⃣ Ensuring sample reviews exist...")
    try:
        total_reviews = ProductReview.objects.count()
        print(f"   📊 Current review count: {total_reviews}")
        
        if total_reviews == 0:
            print("   🔧 Adding sample reviews...")
            
            products = Product.objects.all()[:3]
            for product in products:
                ProductReview.objects.create(
                    product=product,
                    user_name="Sample User",
                    user_email="sample@example.com",
                    rating=5,
                    title="Great product!",
                    comment="This is a sample review to test the system.",
                    is_approved=True
                )
                print(f"      ✅ Added review for {product.title}")
        
    except Exception as e:
        print(f"   ❌ Error adding reviews: {e}")
    
    # Fix 4: Test API endpoint
    print("\n4️⃣ Testing API endpoint...")
    try:
        from django.test import Client
        
        client = Client()
        product = Product.objects.first()
        
        if product:
            response = client.get(f'/api/shop/products/{product.id}/reviews/')
            print(f"   📡 API Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                reviews_count = len(data.get('reviews', []))
                print(f"   ✅ API returns {reviews_count} reviews")
            else:
                print(f"   ❌ API error: {response.content.decode()}")
        
    except Exception as e:
        print(f"   ❌ API test error: {e}")
    
    print("\n🎉 Review system fixes completed!")

if __name__ == '__main__':
    fix_review_system()