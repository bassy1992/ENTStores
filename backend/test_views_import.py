#!/usr/bin/env python
"""
Test if views can be imported without errors
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def test_imports():
    """Test if all imports work"""
    
    print("🧪 Testing imports...")
    
    try:
        print("1️⃣ Testing models import...")
        from shop.models import ProductReview, ReviewHelpfulVote, ReviewImage
        print("   ✅ Models imported successfully")
        
        print("2️⃣ Testing serializers import...")
        from shop.serializers import ProductReviewSerializer, CreateReviewSerializer
        print("   ✅ Serializers imported successfully")
        
        print("3️⃣ Testing views import...")
        from shop.views import ProductReviewListCreateView, vote_on_review
        print("   ✅ Views imported successfully")
        
        print("4️⃣ Testing URL patterns...")
        from shop.urls import urlpatterns
        review_urls = [url for url in urlpatterns if 'review' in str(url.pattern)]
        print(f"   ✅ Found {len(review_urls)} review URL patterns")
        for url in review_urls:
            print(f"      - {url.pattern}")
        
        print("5️⃣ Testing view instantiation...")
        view = ProductReviewListCreateView()
        print("   ✅ View can be instantiated")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_imports()