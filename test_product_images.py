#!/usr/bin/env python3
"""
Test ProductImage URL functionality
"""

import os
import sys
import django

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, ProductImage


def test_product_image_urls():
    """Test adding URL-based product images"""
    print("Testing ProductImage URL functionality...")
    
    # Get a product to add images to
    product = Product.objects.first()
    if not product:
        print("No products found. Please add a product first.")
        return
    
    print(f"Adding images to product: {product.title}")
    
    # Sample image URLs
    image_urls = [
        'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center',
        'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&h=400&fit=crop&crop=center',
        'https://images.unsplash.com/photo-1583743814966-8936f37f4678?w=400&h=400&fit=crop&crop=center'
    ]
    
    # Add images with URLs
    for i, url in enumerate(image_urls):
        image, created = ProductImage.objects.get_or_create(
            product=product,
            order=i,
            defaults={
                'image_url': url,
                'alt_text': f'Product image {i+1}',
                'is_primary': i == 0  # First image is primary
            }
        )
        
        if created:
            print(f"✅ Created image {i+1}: {url}")
        else:
            # Update existing image with URL
            image.image_url = url
            image.alt_text = f'Product image {i+1}'
            image.save()
            print(f"✅ Updated image {i+1}: {url}")
    
    # Test the get_image_url method
    print(f"\nTesting image URLs for {product.title}:")
    for image in product.images.all():
        print(f"  Image {image.order}: {image.get_image_url()}")
    
    print(f"\n✅ ProductImage URL functionality is working!")
    print(f"   Product '{product.title}' now has {product.images.count()} images")


if __name__ == '__main__':
    test_product_image_urls()