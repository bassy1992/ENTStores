#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product

print("Checking product image URLs...")

products = Product.objects.all()
for product in products:
    print(f"Product: {product.title}")
    print(f"  ID: {product.id}")
    print(f"  Image: {product.image}")
    print(f"  Image URL: {product.image.url if product.image else 'No image'}")
    print()

# Test what URLs would be sent to Stripe
print("Testing Stripe image URL conversion...")

test_urls = [
    "/media/products/4.jpg",
    "media/products/4.jpg", 
    "http://localhost:8000/media/products/4.jpg",
    "https://example.com/image.jpg",
    ""
]

for url in test_urls:
    print(f"Original: {url}")
    
    # Apply the same logic as in payment_views.py
    image_url = url
    if image_url:
        if image_url.startswith('/media/'):
            image_url = f"http://localhost:8000{image_url}"
        elif image_url.startswith('media/'):
            image_url = f"http://localhost:8000/{image_url}"
    
    valid = image_url and (image_url.startswith('http://') or image_url.startswith('https://'))
    print(f"  Converted: {image_url}")
    print(f"  Valid for Stripe: {valid}")
    print()