#!/usr/bin/env python3
"""
Test script to check product API data.
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product
from shop.serializers import ProductSerializer
from django.test import RequestFactory

def test_product_api():
    # Get a product
    product = Product.objects.filter(title__icontains='jkhjkhjk').first()
    if not product:
        print('Product "jkhjkhjk" not found')
        return
    
    print(f'Testing product: {product.title}')
    
    # Create a mock request for the serializer
    factory = RequestFactory()
    request = factory.get('/')
    
    # Serialize the product
    serializer = ProductSerializer(product, context={'request': request})
    data = serializer.data
    
    print(f'Available sizes: {len(data.get("available_sizes", []))}')
    for size in data.get("available_sizes", []):
        print(f'  - {size.get("display_name")} ({size.get("name")})')
    
    print(f'Available colors: {len(data.get("available_colors", []))}')
    for color in data.get("available_colors", []):
        print(f'  - {color.get("name")} ({color.get("hex_code")})')
    
    print(f'Variants: {len(data.get("variants", []))}')
    for variant in data.get('variants', []):
        size_name = variant.get("size", {}).get("display_name", "No size")
        color_name = variant.get("color", {}).get("name", "No color")
        stock = variant.get("stock_quantity", 0)
        available = variant.get("is_available", False)
        in_stock = variant.get("is_in_stock", False)
        print(f'  - {size_name} - {color_name}: Stock={stock}, Available={available}, InStock={in_stock}')

if __name__ == '__main__':
    test_product_api()