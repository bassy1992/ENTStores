#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product
from django.db.models import Q

# Check all products first
all_products = Product.objects.all()
print(f"Total products in database: {all_products.count()}")

# Find products with 'shorts' in the title
shorts_products = Product.objects.filter(title__icontains='shorts')
print(f"\nFound {shorts_products.count()} products with 'shorts' in title:")
for product in shorts_products:
    print(f"- {product.title} (slug: {product.slug})")

# Find the coral pink shorts product by different searches
coral_products = Product.objects.filter(Q(title__icontains='coral') | Q(slug__icontains='coral'))
print(f"\nFound {coral_products.count()} products matching 'coral':")
for product in coral_products:
    print(f"- {product.title} (slug: {product.slug})")

# Check products with pink
pink_products = Product.objects.filter(Q(title__icontains='pink') | Q(slug__icontains='pink'))
print(f"\nFound {pink_products.count()} products matching 'pink':")
for product in pink_products:
    print(f"- {product.title} (slug: {product.slug})")

# Show first 10 products to see what's in the database
print(f"\nFirst 10 products in database:")
for product in all_products[:10]:
    print(f"- {product.title} (slug: {product.slug}, stock: {product.stock_quantity})")

