#!/usr/bin/env python3
"""
Script to add products with URL-based images
This script helps you easily add products using image URLs instead of uploading files
"""

import os
import sys
import django
import json

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, Category


def add_product_with_url(product_data):
    """Add a single product with URL-based image"""
    try:
        # Check if category exists
        category = Category.objects.get(key=product_data['category'])
        
        # Create or update product
        product, created = Product.objects.update_or_create(
            id=product_data['id'],
            defaults={
                'title': product_data['title'],
                'price': product_data['price'],
                'description': product_data['description'],
                'image_url': product_data['image_url'],  # Use URL instead of file
                'category': category,
                'stock_quantity': product_data.get('stock_quantity', 0),
                'is_featured': product_data.get('is_featured', False),
                'is_active': product_data.get('is_active', True),
            }
        )
        
        action = "Created" if created else "Updated"
        print(f"✅ {action} product: {product.title} (ID: {product.id})")
        print(f"   Image URL: {product.image_url}")
        return product
        
    except Category.DoesNotExist:
        print(f"❌ Category '{product_data['category']}' not found for product {product_data['id']}")
        return None
    except Exception as e:
        print(f"❌ Error adding product {product_data['id']}: {e}")
        return None


def load_products_from_json(file_path):
    """Load products from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {file_path}: {e}")
        return []


def add_sample_url_products():
    """Add sample products with URLs from the existing JSON file"""
    print("🚀 Adding sample products with URL-based images...")
    
    # Load from existing sample file
    products_data = load_products_from_json('backend/sample_products_with_urls.json')
    
    if not products_data:
        print("❌ No products data found")
        return
    
    success_count = 0
    for product_data in products_data:
        if add_product_with_url(product_data):
            success_count += 1
    
    print(f"\n✅ Successfully added/updated {success_count} out of {len(products_data)} products")


def add_custom_product():
    """Interactive function to add a custom product with URL"""
    print("\n📝 Add a custom product with URL-based image")
    print("=" * 50)
    
    # Get product details
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("❌ Product ID is required")
        return
    
    title = input("Product Title: ").strip()
    if not title:
        print("❌ Product title is required")
        return
    
    try:
        price = float(input("Price ($): ").strip())
    except ValueError:
        print("❌ Invalid price")
        return
    
    description = input("Description: ").strip()
    if not description:
        print("❌ Description is required")
        return
    
    image_url = input("Image URL: ").strip()
    if not image_url:
        print("❌ Image URL is required")
        return
    
    # Show available categories
    print("\nAvailable categories:")
    categories = Category.objects.all()
    for cat in categories:
        print(f"  - {cat.key}: {cat.label}")
    
    category_key = input("Category key: ").strip()
    if not category_key:
        print("❌ Category is required")
        return
    
    try:
        stock_quantity = int(input("Stock quantity (default 0): ").strip() or "0")
    except ValueError:
        stock_quantity = 0
    
    is_featured = input("Is featured? (y/N): ").strip().lower() == 'y'
    
    # Create product data
    product_data = {
        'id': product_id,
        'title': title,
        'price': str(price),
        'description': description,
        'image_url': image_url,
        'category': category_key,
        'stock_quantity': stock_quantity,
        'is_featured': is_featured,
        'is_active': True
    }
    
    # Add the product
    product = add_product_with_url(product_data)
    if product:
        print(f"\n✅ Product added successfully!")
        print(f"   View at: /api/products/{product.id}/")


def main():
    """Main function"""
    print("🛍️  URL-Based Product Manager")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Add sample products from JSON")
        print("2. Add custom product")
        print("3. List existing products")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            add_sample_url_products()
        elif choice == '2':
            add_custom_product()
        elif choice == '3':
            print("\n📋 Existing products:")
            products = Product.objects.all()
            for product in products:
                image_source = "URL" if product.image_url else "File" if product.image else "None"
                print(f"  - {product.id}: {product.title} (Image: {image_source})")
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option")


if __name__ == '__main__':
    main()