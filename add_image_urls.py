#!/usr/bin/env python3
"""
Add Image URLs to Products
Interactive script to add image URLs to your existing products
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

from shop.models import Product, Category


def show_products_without_images():
    """Show products that don't have image URLs"""
    print("Products without image URLs:")
    print("=" * 35)
    
    products = Product.objects.filter(
        models.Q(image_url__isnull=True) | models.Q(image_url='')
    )
    
    for i, product in enumerate(products, 1):
        image_status = "File" if product.image else "None"
        print(f"{i}. {product.id}: {product.title}")
        print(f"   Current image: {image_status}")
        print(f"   Category: {product.category.label}")
        print()
    
    return products


def add_url_to_product(product_id, image_url):
    """Add image URL to a specific product"""
    try:
        product = Product.objects.get(id=product_id)
        product.image_url = image_url
        product.save()
        print(f"✅ Updated {product.title} with image URL")
        return True
    except Product.DoesNotExist:
        print(f"❌ Product {product_id} not found")
        return False
    except Exception as e:
        print(f"❌ Error updating product: {e}")
        return False


def bulk_add_urls():
    """Add URLs to multiple products at once"""
    print("Bulk Add Image URLs")
    print("=" * 25)
    
    # Suggested URLs for different categories
    suggested_urls = {
        't-shirts': [
            'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center',
            'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&h=400&fit=crop&crop=center',
            'https://images.unsplash.com/photo-1583743814966-8936f37f4678?w=400&h=400&fit=crop&crop=center'
        ],
        'hoodies': [
            'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop&crop=center',
            'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop&crop=center',
            'https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=400&h=400&fit=crop&crop=center'
        ],
        'polos': [
            'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop&crop=center',
            'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=400&fit=crop&crop=center'
        ],
        'jackets': [
            'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop&crop=center',
            'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop&crop=center'
        ]
    }
    
    products_without_urls = Product.objects.filter(
        models.Q(image_url__isnull=True) | models.Q(image_url='')
    )
    
    updated_count = 0
    for product in products_without_urls:
        category_key = product.category.key
        
        if category_key in suggested_urls:
            # Use the first available URL for this category
            url_index = updated_count % len(suggested_urls[category_key])
            image_url = suggested_urls[category_key][url_index]
            
            product.image_url = image_url
            product.save()
            
            print(f"✅ {product.title}: {image_url}")
            updated_count += 1
        else:
            print(f"⚠️  {product.title}: No suggested URL for category '{category_key}'")
    
    print(f"\n✅ Updated {updated_count} products with image URLs")


def interactive_add():
    """Interactive mode to add URLs one by one"""
    print("Interactive Image URL Addition")
    print("=" * 35)
    
    products = show_products_without_images()
    
    if not products:
        print("✅ All products already have image URLs!")
        return
    
    print("Enter image URLs for products (press Enter to skip):")
    print("Suggested format: https://images.unsplash.com/photo-123?w=400&h=400&fit=crop")
    print()
    
    for product in products:
        print(f"Product: {product.title}")
        print(f"Category: {product.category.label}")
        
        url = input("Image URL (or Enter to skip): ").strip()
        
        if url:
            if add_url_to_product(product.id, url):
                print("✅ Added successfully!")
            else:
                print("❌ Failed to add URL")
        else:
            print("⏭️  Skipped")
        
        print()


def main():
    """Main function"""
    print("🖼️  Product Image URL Manager")
    print("=" * 35)
    
    while True:
        print("\nOptions:")
        print("1. Show products without image URLs")
        print("2. Bulk add suggested URLs")
        print("3. Interactive URL addition")
        print("4. Add URL to specific product")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            show_products_without_images()
        
        elif choice == '2':
            bulk_add_urls()
        
        elif choice == '3':
            interactive_add()
        
        elif choice == '4':
            product_id = input("Enter product ID: ").strip()
            image_url = input("Enter image URL: ").strip()
            
            if product_id and image_url:
                add_url_to_product(product_id, image_url)
            else:
                print("❌ Both product ID and image URL are required")
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")


if __name__ == '__main__':
    # Import models for filtering
    from django.db import models
    main()