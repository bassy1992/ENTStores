#!/usr/bin/env python
"""
Debug the review view logic
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
from shop.views import ProductReviewListCreateView
from django.test import RequestFactory

def debug_review_view():
    """Debug the review view"""
    
    # Get a product
    product = Product.objects.first()
    print(f"🧪 Debugging review view for product: {product.title} (ID: {product.id})")
    
    # Test the queryset directly
    print("\n1️⃣ Testing queryset directly...")
    queryset = ProductReview.objects.filter(
        product_id=product.id,
        is_approved=True
    ).select_related('product')
    
    print(f"   Raw queryset count: {queryset.count()}")
    for review in queryset[:3]:
        print(f"   - {review.user_name}: {review.title} (approved: {review.is_approved})")
    
    # Test the view's get_queryset method
    print("\n2️⃣ Testing view's get_queryset method...")
    try:
        factory = RequestFactory()
        request = factory.get(f'/api/shop/products/{product.id}/reviews/')
        
        view = ProductReviewListCreateView()
        view.request = request
        view.kwargs = {'product_id': product.id}
        
        view_queryset = view.get_queryset()
        print(f"   View queryset count: {view_queryset.count()}")
        
        for review in view_queryset[:3]:
            print(f"   - {review.user_name}: {review.title}")
            
    except Exception as e:
        print(f"   ❌ Error testing view: {e}")
        import traceback
        traceback.print_exc()
    
    # Test the serializer
    print("\n3️⃣ Testing serializer...")
    try:
        from shop.serializers import ProductReviewSerializer
        
        reviews = ProductReview.objects.filter(product_id=product.id, is_approved=True)[:2]
        serializer = ProductReviewSerializer(reviews, many=True)
        
        print(f"   Serialized {len(serializer.data)} reviews")
        if serializer.data:
            first_review = serializer.data[0]
            print(f"   First review keys: {list(first_review.keys())}")
            print(f"   First review: {first_review.get('user_name')} - {first_review.get('title')}")
            
    except Exception as e:
        print(f"   ❌ Serializer error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test the stats calculation
    print("\n4️⃣ Testing stats calculation...")
    try:
        view = ProductReviewListCreateView()
        stats = view.get_review_stats(product.id)
        print(f"   Stats: {stats}")
        
    except Exception as e:
        print(f"   ❌ Stats error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_review_view()