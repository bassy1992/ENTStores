#!/usr/bin/env python3
"""
Quick Add Image URLs to Products
Simple script to add image URLs to products without them
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

from shop.models import Product
from django.db import models


def add_urls_to_products():
    """Add image URLs to products that don't have them"""
    
    # High-quality Unsplash URLs for different product types
    image_urls = [
        'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center',  # Black t-shirt
        'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&h=400&fit=crop&crop=center',  # White t-shirt
        'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop&crop=center',  # Hoodie
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop&crop=center',  # Grey hoodie
        'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop&crop=center',  # Polo shirt
        'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop&crop=center',  # Jacket
        'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&h=400&fit=crop&crop=center',  # Shorts
        'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=400&fit=crop&crop=center',  # Cap
        'https://images.unsplash.com/photo-1506629905607-d9f02a6a0e7b?w=400&h=400&fit=crop&crop=center',  # Tracksuit
        'https://images.unsplash.com/photo-1583743814966-8936f37f4678?w=400&h=400&fit=crop&crop=center',  # T-shirt variant
    ]
    
    # Get products without image URLs
    products_without_urls = Product.objects.filter(
        models.Q(image_url__isnull=True) | models.Q(image_url='')
    )
    
    print(f"Found {products_without_urls.count()} products without image URLs")
    print("Adding URLs...")
    print()
    
    updated_count = 0
    for i, product in enumerate(products_without_urls):
        # Cycle through available URLs
        url_index = i % len(image_urls)
        image_url = image_urls[url_index]
        
        # Update product
        product.image_url = image_url
        product.save()
        
        print(f"✅ {product.title}")
        print(f"   URL: {image_url}")
        print()
        
        updated_count += 1
    
    print(f"✅ Updated {updated_count} products with image URLs!")
    return updated_count


def show_products_status():
    """Show current status of products"""
    total_products = Product.objects.count()
    products_with_urls = Product.objects.filter(
        image_url__isnull=False
    ).exclude(image_url='').count()
    
    products_without_urls = total_products - products_with_urls
    
    print("Product Image Status:")
    print("=" * 25)
    print(f"Total products: {total_products}")
    print(f"With image URLs: {products_with_urls}")
    print(f"Without URLs: {products_without_urls}")
    
    if products_without_urls > 0:
        print(f"\nProducts needing URLs:")
        products = Product.objects.filter(
            models.Q(image_url__isnull=True) | models.Q(image_url='')
        )[:5]  # Show first 5
        
        for product in products:
            print(f"  - {product.id}: {product.title}")
        
        if products_without_urls > 5:
            print(f"  ... and {products_without_urls - 5} more")


def main():
    """Main function"""
    print("🖼️  Quick Image URL Manager")
    print("=" * 30)
    
    show_products_status()
    
    products_without_urls = Product.objects.filter(
        models.Q(image_url__isnull=True) | models.Q(image_url='')
    ).count()
    
    if products_without_urls > 0:
        print(f"\nDo you want to add image URLs to {products_without_urls} products? (y/n): ", end="")
        response = input().strip().lower()
        
        if response == 'y':
            add_urls_to_products()
        else:
            print("No changes made.")
    else:
        print("\n✅ All products already have image URLs!")


if __name__ == '__main__':
    main()