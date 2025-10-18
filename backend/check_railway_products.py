#!/usr/bin/env python
"""
Check products in Railway database
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, Category

def check_products():
    """Check what products exist in the database"""
    
    print("🔍 Checking Railway Database Products...")
    print("=" * 50)
    
    # Check total counts
    product_count = Product.objects.count()
    category_count = Category.objects.count()
    
    print(f"📊 Total Products: {product_count}")
    print(f"📁 Total Categories: {category_count}")
    print()
    
    if product_count == 0:
        print("❌ No products found in database!")
        return
    
    # List all products
    print("📋 Products in database:")
    for product in Product.objects.all():
        image_status = "📷 URL" if product.image_url else ("📁 File" if product.image else "❌ No Image")
        featured = "⭐" if product.is_featured else "  "
        
        print(f"{featured} {product.id}: {product.title}")
        print(f"   💰 ${product.price} | 📦 Stock: {product.stock_quantity} | {image_status}")
        if product.image_url:
            print(f"   🔗 {product.image_url[:60]}...")
        print()
    
    # Check categories
    print("📁 Categories:")
    for category in Category.objects.all():
        product_count = category.products.count()
        print(f"   {category.key}: {category.label} ({product_count} products)")

if __name__ == '__main__':
    check_products()