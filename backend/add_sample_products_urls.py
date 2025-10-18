#!/usr/bin/env python
"""
Script to add sample products with image URLs
"""

import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, Category
from decimal import Decimal

def add_products_from_json():
    """Add products from the sample JSON file"""
    
    # Load the JSON data
    with open('sample_products_with_urls.json', 'r') as f:
        products_data = json.load(f)
    
    print(f"🛍️  Adding {len(products_data)} products with image URLs...")
    print("=" * 50)
    
    created_count = 0
    updated_count = 0
    
    for product_data in products_data:
        try:
            # Get or create category
            category, cat_created = Category.objects.get_or_create(
                key=product_data['category'],
                defaults={
                    'label': product_data['category'].replace('-', ' ').title(),
                    'description': f'{product_data["category"].replace("-", " ").title()} category'
                }
            )
            
            if cat_created:
                print(f"📁 Created category: {category.label}")
            
            # Create or update product
            product, created = Product.objects.get_or_create(
                id=product_data['id'],
                defaults={
                    'title': product_data['title'],
                    'price': Decimal(str(product_data['price'])),
                    'description': product_data['description'],
                    'image_url': product_data['image_url'],
                    'category': category,
                    'stock_quantity': product_data.get('stock_quantity', 10),
                    'is_featured': product_data.get('is_featured', False),
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                print(f"✅ Created: {product.title} - ${product.price}")
            else:
                # Update existing product
                product.title = product_data['title']
                product.price = Decimal(str(product_data['price']))
                product.description = product_data['description']
                product.image_url = product_data['image_url']
                product.category = category
                product.stock_quantity = product_data.get('stock_quantity', product.stock_quantity)
                product.is_featured = product_data.get('is_featured', product.is_featured)
                product.save()
                
                updated_count += 1
                print(f"🔄 Updated: {product.title} - ${product.price}")
                
        except Exception as e:
            print(f"❌ Error with product {product_data.get('id', 'unknown')}: {e}")
    
    print("=" * 50)
    print(f"🎉 Completed! Created: {created_count}, Updated: {updated_count}")
    print(f"📊 Total products in database: {Product.objects.count()}")
    
    # Show featured products
    featured = Product.objects.filter(is_featured=True)
    if featured.exists():
        print(f"⭐ Featured products: {featured.count()}")
        for product in featured:
            print(f"   - {product.title}")

if __name__ == '__main__':
    add_products_from_json()