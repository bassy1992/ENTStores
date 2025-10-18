#!/usr/bin/env python3
"""
Demo: Multiple Product Images with URLs
Shows how to add multiple images to a single product using URLs
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

from shop.models import Product, ProductImage, Category


def demo_multiple_images():
    """Demonstrate adding multiple images to a product"""
    print("🖼️  Multiple Product Images Demo")
    print("=" * 35)
    
    # Get or create a demo product
    category, _ = Category.objects.get_or_create(
        key='t-shirts',
        defaults={
            'label': 'T-Shirts',
            'description': 'Comfortable t-shirts for everyday wear'
        }
    )
    
    product, created = Product.objects.get_or_create(
        id='demo-multi-image-product',
        defaults={
            'title': 'Demo Multi-Image T-Shirt',
            'price': '29.99',
            'description': 'Demo product showing multiple image support',
            'category': category,
            'stock_quantity': 10,
            'is_active': True
        }
    )
    
    action = "Created" if created else "Found existing"
    print(f"{action} demo product: {product.title}")
    
    # Clear existing images for clean demo
    product.images.all().delete()
    
    # Add multiple images with URLs
    image_data = [
        {
            'url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center',
            'alt_text': 'Front view of black t-shirt',
            'is_primary': True,
            'order': 1
        },
        {
            'url': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&h=400&fit=crop&crop=center',
            'alt_text': 'Back view of white t-shirt',
            'is_primary': False,
            'order': 2
        },
        {
            'url': 'https://images.unsplash.com/photo-1583743814966-8936f37f4678?w=400&h=400&fit=crop&crop=center',
            'alt_text': 'Side view of gray t-shirt',
            'is_primary': False,
            'order': 3
        },
        {
            'url': 'https://images.unsplash.com/photo-1571945153237-4929e783af4a?w=400&h=400&fit=crop&crop=center',
            'alt_text': 'Detail view of t-shirt fabric',
            'is_primary': False,
            'order': 4
        },
        {
            'url': 'https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400&h=400&fit=crop&crop=center',
            'alt_text': 'T-shirt worn by model',
            'is_primary': False,
            'order': 5
        }
    ]
    
    print(f"\nAdding {len(image_data)} images to product...")
    
    for i, img_data in enumerate(image_data, 1):
        image = ProductImage.objects.create(
            product=product,
            image_url=img_data['url'],
            alt_text=img_data['alt_text'],
            is_primary=img_data['is_primary'],
            order=img_data['order']
        )
        
        primary_indicator = " (PRIMARY)" if img_data['is_primary'] else ""
        print(f"  ✅ Image {i}: {img_data['alt_text']}{primary_indicator}")
        print(f"     URL: {img_data['url']}")
    
    # Show the results
    print(f"\n📊 Product Image Summary:")
    print(f"   Product: {product.title}")
    print(f"   Total Images: {product.images.count()}")
    
    print(f"\n🖼️  All Images for '{product.title}':")
    for image in product.images.all().order_by('order'):
        primary_text = " [PRIMARY]" if image.is_primary else ""
        print(f"   {image.order}. {image.alt_text}{primary_text}")
        print(f"      URL: {image.get_image_url()}")
    
    # Show how to access images in code
    print(f"\n💻 Code Examples:")
    print(f"   # Get all images: product.images.all()")
    print(f"   # Get primary image: product.images.filter(is_primary=True).first()")
    print(f"   # Get image URLs: [img.get_image_url() for img in product.images.all()]")
    
    # Test the methods
    primary_image = product.images.filter(is_primary=True).first()
    if primary_image:
        print(f"\n🎯 Primary Image: {primary_image.alt_text}")
        print(f"   URL: {primary_image.get_image_url()}")
    
    all_urls = [img.get_image_url() for img in product.images.all()]
    print(f"\n📋 All Image URLs ({len(all_urls)} total):")
    for i, url in enumerate(all_urls, 1):
        print(f"   {i}. {url}")
    
    print(f"\n✅ Multiple images demo completed!")
    print(f"\n🔧 Django Admin Instructions:")
    print(f"   1. Go to /admin/shop/product/")
    print(f"   2. Edit '{product.title}'")
    print(f"   3. Scroll to 'Product Images' section")
    print(f"   4. You'll see {product.images.count()} existing images")
    print(f"   5. Add more by filling 'Image URL' fields")
    print(f"   6. Set 'Is primary' for main image")
    print(f"   7. Use 'Order' to control display sequence")


if __name__ == '__main__':
    demo_multiple_images()