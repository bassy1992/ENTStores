#!/usr/bin/env python3
"""
Test script for URL-based images functionality
"""

import os
import sys
import django
import requests

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, Category


def test_image_url_accessibility(url):
    """Test if an image URL is accessible"""
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except Exception as e:
        return False


def test_product_image_methods():
    """Test product image URL methods"""
    print("🧪 Testing Product Image URL Methods")
    print("=" * 40)
    
    # Get products with image URLs
    products_with_urls = Product.objects.filter(image_url__isnull=False).exclude(image_url='')
    
    if not products_with_urls:
        print("❌ No products with image URLs found")
        print("   Run 'python add_url_based_products.py' to add sample products")
        return
    
    for product in products_with_urls[:5]:  # Test first 5 products
        print(f"\n📦 Testing: {product.title}")
        print(f"   ID: {product.id}")
        print(f"   Image URL: {product.image_url}")
        
        # Test get_image_url method
        image_url = product.get_image_url()
        print(f"   get_image_url(): {image_url}")
        
        # Test URL accessibility
        if test_image_url_accessibility(image_url):
            print("   ✅ Image URL is accessible")
        else:
            print("   ❌ Image URL is not accessible")
        
        # Test display_image_url property
        display_url = product.display_image_url
        print(f"   display_image_url: {display_url}")


def test_api_response():
    """Test API response for products with URL images"""
    print("\n🌐 Testing API Response")
    print("=" * 25)
    
    from shop.serializers import ProductSerializer
    from django.test import RequestFactory
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/api/products/')
    
    # Get a product with image URL
    product = Product.objects.filter(image_url__isnull=False).exclude(image_url='').first()
    
    if not product:
        print("❌ No products with image URLs found for API test")
        return
    
    # Serialize the product
    serializer = ProductSerializer(product, context={'request': request})
    data = serializer.data
    
    print(f"📦 Product: {data['title']}")
    print(f"   API Image Field: {data.get('image', 'Not found')}")
    print(f"   Expected URL: {product.image_url}")
    
    if data.get('image') == product.image_url:
        print("   ✅ API correctly returns image URL")
    else:
        print("   ❌ API image field doesn't match expected URL")


def test_fallback_behavior():
    """Test image fallback behavior"""
    print("\n🔄 Testing Fallback Behavior")
    print("=" * 30)
    
    # Test product with no images
    product_no_image = Product.objects.filter(
        image__isnull=True, 
        image_url__isnull=True
    ).first()
    
    if product_no_image:
        fallback_url = product_no_image.get_image_url()
        print(f"📦 Product with no image: {product_no_image.title}")
        print(f"   Fallback URL: {fallback_url}")
        
        if "placeholder" in fallback_url:
            print("   ✅ Correctly returns placeholder image")
        else:
            print("   ❌ Fallback not working correctly")
    else:
        print("   ℹ️  No products without images found")
    
    # Test product with both file and URL (file should take priority)
    product_both = Product.objects.filter(
        image__isnull=False, 
        image_url__isnull=False
    ).exclude(image_url='').first()
    
    if product_both:
        image_url = product_both.get_image_url()
        print(f"\n📦 Product with both file and URL: {product_both.title}")
        print(f"   Returned URL: {image_url}")
        print(f"   File URL: {product_both.image.url if product_both.image else 'None'}")
        print(f"   URL field: {product_both.image_url}")
        
        if product_both.image and product_both.image.url in image_url:
            print("   ✅ Correctly prioritizes uploaded file")
        elif product_both.image_url in image_url:
            print("   ✅ Uses URL field (no uploaded file)")
        else:
            print("   ❌ Unexpected behavior")


def create_test_product():
    """Create a test product with URL image"""
    print("\n➕ Creating Test Product")
    print("=" * 25)
    
    test_image_url = "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center"
    
    # Check if test category exists
    try:
        category = Category.objects.get(key='t-shirts')
    except Category.DoesNotExist:
        print("❌ T-shirts category not found. Creating it...")
        category = Category.objects.create(
            key='t-shirts',
            label='T-Shirts',
            description='Comfortable t-shirts for everyday wear'
        )
    
    # Create test product
    product, created = Product.objects.update_or_create(
        id='test-url-product',
        defaults={
            'title': 'Test URL Product',
            'price': '19.99',
            'description': 'Test product with URL-based image',
            'image_url': test_image_url,
            'category': category,
            'stock_quantity': 10,
            'is_active': True
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"✅ {action} test product: {product.title}")
    print(f"   Image URL: {product.image_url}")
    
    # Test the image URL
    if test_image_url_accessibility(test_image_url):
        print("   ✅ Test image URL is accessible")
    else:
        print("   ❌ Test image URL is not accessible")
    
    return product


def main():
    """Main test function"""
    print("🧪 URL-Based Images Test Suite")
    print("=" * 40)
    
    # Run tests
    test_product_image_methods()
    test_api_response()
    test_fallback_behavior()
    
    # Create test product if needed
    if not Product.objects.filter(image_url__isnull=False).exclude(image_url='').exists():
        print("\n📝 No products with URLs found. Creating test product...")
        create_test_product()
        print("\n🔄 Re-running tests with test product...")
        test_product_image_methods()
        test_api_response()
    
    print("\n✅ Test suite completed!")
    print("\nNext steps:")
    print("1. Run 'python add_url_based_products.py' to add more products")
    print("2. Check Django Admin to manage products")
    print("3. Test your frontend to ensure images load correctly")


if __name__ == '__main__':
    main()