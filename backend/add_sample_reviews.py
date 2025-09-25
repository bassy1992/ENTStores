#!/usr/bin/env python
"""
Add sample reviews to test the review system
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, ProductReview

def add_sample_reviews():
    """Add sample reviews for testing"""
    
    # Get a product to add reviews to
    try:
        # Try to get the green faster than light product
        product = Product.objects.filter(slug__icontains='green-faster').first()
        if not product:
            # Get any active product
            product = Product.objects.filter(is_active=True).first()
        
        if not product:
            print("❌ No products found. Please add products first.")
            return
        
        print(f"📝 Adding sample reviews for product: {product.title}")
        
        # Sample reviews data
        sample_reviews = [
            {
                'user_name': 'Sarah M.',
                'user_email': 'sarah.m@example.com',
                'rating': 5,
                'title': 'Amazing quality!',
                'comment': 'This product exceeded my expectations. The material is soft and comfortable, and the fit is perfect. I\'ve washed it several times and it still looks brand new. Highly recommend!',
                'size_purchased': 'M',
                'color_purchased': 'Green',
                'verified_purchase': True
            },
            {
                'user_name': 'Mike R.',
                'user_email': 'mike.r@example.com',
                'rating': 4,
                'title': 'Good value for money',
                'comment': 'Nice product overall. The color is exactly as shown in the pictures. Only minor complaint is that it runs slightly small, so consider sizing up.',
                'size_purchased': 'L',
                'color_purchased': 'Green',
                'verified_purchase': True
            },
            {
                'user_name': 'Jennifer K.',
                'user_email': 'jennifer.k@example.com',
                'rating': 5,
                'title': 'Perfect fit and style',
                'comment': 'Love this! The design is exactly what I was looking for. Fast shipping and great customer service too.',
                'size_purchased': 'S',
                'color_purchased': 'Green',
                'verified_purchase': True
            },
            {
                'user_name': 'David L.',
                'user_email': 'david.l@example.com',
                'rating': 3,
                'title': 'Decent but not exceptional',
                'comment': 'It\'s okay. The quality is decent for the price, but I\'ve seen better. The color faded a bit after a few washes.',
                'size_purchased': 'XL',
                'color_purchased': 'Green',
                'verified_purchase': False
            },
            {
                'user_name': 'Emma S.',
                'user_email': 'emma.s@example.com',
                'rating': 5,
                'title': 'Excellent purchase!',
                'comment': 'Really happy with this purchase. The fabric feels premium and the fit is true to size. Will definitely buy more colors.',
                'size_purchased': 'M',
                'color_purchased': 'Green',
                'verified_purchase': True
            }
        ]
        
        created_count = 0
        for i, review_data in enumerate(sample_reviews):
            # Check if review already exists
            existing_review = ProductReview.objects.filter(
                product=product,
                user_email=review_data['user_email']
            ).first()
            
            if existing_review:
                print(f"⚠️  Review by {review_data['user_name']} already exists, skipping...")
                continue
            
            # Create the review with a date in the past
            created_at = datetime.now() - timedelta(days=10-i)
            
            review = ProductReview.objects.create(
                product=product,
                user_name=review_data['user_name'],
                user_email=review_data['user_email'],
                rating=review_data['rating'],
                title=review_data['title'],
                comment=review_data['comment'],
                size_purchased=review_data['size_purchased'],
                color_purchased=review_data['color_purchased'],
                verified_purchase=review_data['verified_purchase'],
                is_approved=True
            )
            
            # Update the created_at timestamp
            review.created_at = created_at
            review.save()
            
            created_count += 1
            print(f"✅ Created review by {review_data['user_name']} ({review_data['rating']} stars)")
        
        print(f"\n🎉 Successfully created {created_count} sample reviews for {product.title}")
        
        # Show review statistics
        total_reviews = ProductReview.objects.filter(product=product, is_approved=True).count()
        avg_rating = ProductReview.objects.filter(product=product, is_approved=True).aggregate(
            avg_rating=django.db.models.Avg('rating')
        )['avg_rating']
        
        print(f"📊 Product now has {total_reviews} reviews with average rating: {avg_rating:.1f}")
        
    except Exception as e:
        print(f"❌ Error adding sample reviews: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    add_sample_reviews()