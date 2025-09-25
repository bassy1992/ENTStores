#!/usr/bin/env python
"""
Migrate review system to production
This script should be run on the production server (Render)
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from shop.models import Product, ProductReview

def migrate_production_reviews():
    """Migrate review system to production"""
    
    print("🚀 Migrating review system to production...")
    
    # Step 1: Create migrations
    print("\n1️⃣ Creating migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'shop'])
        print("   ✅ Migrations created")
    except Exception as e:
        print(f"   ⚠️ Migration creation: {e}")
    
    # Step 2: Run migrations
    print("\n2️⃣ Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("   ✅ Migrations applied")
    except Exception as e:
        print(f"   ❌ Migration failed: {e}")
        return
    
    # Step 3: Check if tables exist
    print("\n3️⃣ Verifying tables...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE '%review%'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
        if tables:
            print(f"   ✅ Review tables created:")
            for table in tables:
                print(f"      - {table[0]}")
        else:
            print("   ❌ Review tables not found")
            return
            
    except Exception as e:
        print(f"   ❌ Error checking tables: {e}")
        return
    
    # Step 4: Add sample reviews
    print("\n4️⃣ Adding sample reviews...")
    try:
        # Check if we have products
        products = Product.objects.all()[:3]
        if not products:
            print("   ⚠️ No products found, skipping sample reviews")
            return
        
        # Add sample reviews for each product
        sample_reviews_data = [
            {
                'user_name': 'Sarah M.',
                'user_email': 'sarah.m@example.com',
                'rating': 5,
                'title': 'Amazing quality!',
                'comment': 'This product exceeded my expectations. The material is soft and comfortable, and the fit is perfect.',
                'verified_purchase': True,
                'size_purchased': 'M',
                'color_purchased': 'Black'
            },
            {
                'user_name': 'Mike R.',
                'user_email': 'mike.r@example.com',
                'rating': 4,
                'title': 'Good value for money',
                'comment': 'Nice product overall. The color is exactly as shown in the pictures.',
                'verified_purchase': True,
                'size_purchased': 'L',
                'color_purchased': 'Black'
            },
            {
                'user_name': 'Jennifer K.',
                'user_email': 'jennifer.k@example.com',
                'rating': 5,
                'title': 'Perfect fit and style',
                'comment': 'Love this! The design is exactly what I was looking for.',
                'verified_purchase': True,
                'size_purchased': 'S',
                'color_purchased': 'Black'
            }
        ]
        
        created_count = 0
        for product in products:
            for i, review_data in enumerate(sample_reviews_data):
                # Check if review already exists
                existing = ProductReview.objects.filter(
                    product=product,
                    user_email=review_data['user_email']
                ).first()
                
                if not existing:
                    review = ProductReview.objects.create(
                        product=product,
                        **review_data,
                        is_approved=True
                    )
                    created_count += 1
                    print(f"      ✅ Created review by {review_data['user_name']} for {product.title}")
        
        print(f"   🎉 Created {created_count} sample reviews")
        
    except Exception as e:
        print(f"   ❌ Error creating sample reviews: {e}")
    
    # Step 5: Verify reviews
    print("\n5️⃣ Verifying reviews...")
    try:
        total_reviews = ProductReview.objects.count()
        print(f"   📊 Total reviews in database: {total_reviews}")
        
        if total_reviews > 0:
            # Show sample reviews
            sample_reviews = ProductReview.objects.all()[:5]
            for review in sample_reviews:
                print(f"      - {review.user_name}: {review.title} ({review.rating}★)")
        
    except Exception as e:
        print(f"   ❌ Error verifying reviews: {e}")
    
    print("\n🎉 Production review system migration completed!")
    print("\n📋 Next steps:")
    print("   1. Check Django admin: /admin/shop/productreview/")
    print("   2. Test frontend review loading")
    print("   3. Test review submission")

if __name__ == '__main__':
    migrate_production_reviews()