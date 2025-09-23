#!/usr/bin/env python3
"""
Script to add sample categories with images to the database.
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Category

def add_sample_categories():
    """Add sample categories with images."""
    
    categories_data = [
        {
            'key': 't-shirts',
            'label': 'T-Shirts',
            'description': 'Premium cotton tees with signature designs and comfortable fits',
            'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=600',
            'featured': True,
        },
        {
            'key': 'polos',
            'label': 'Polos',
            'description': 'Classic polo shirts for smart-casual occasions',
            'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Ff6d93005cb0342e0ae5980da9f131c00?format=webp&width=600',
            'featured': False,
        },
        {
            'key': 'hoodies',
            'label': 'Hoodies / Crewnecks',
            'description': 'Cozy hoodies and crewnecks for everyday comfort',
            'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F65c976a3ea2e4593b4d1a27829d0f390?format=webp&width=600',
            'featured': True,
        },
        {
            'key': 'sweatshirts',
            'label': 'Sweatshirts',
            'description': 'Warm and stylish sweatshirts for cooler days',
            'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=600',
            'featured': False,
        },
        {
            'key': 'tracksuits',
            'label': 'Tracksuits',
            'description': 'Athletic tracksuits for sport and street style',
            'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F690488dfe67548ada8fe07090b86601f?format=webp&width=600',
            'featured': True,
        },
        {
            'key': 'jackets',
            'label': 'Jackets',
            'description': 'Versatile jackets for all seasons and occasions',
            'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F0c4ab9be3dd740618a71b6809f4d5f28?format=webp&width=600',
            'featured': False,
        },
        {
            'key': 'shorts',
            'label': 'Shorts',
            'description': 'Comfortable shorts for active lifestyles',
            'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=600',
            'featured': False,
        },
        {
            'key': 'headwear',
            'label': 'Headwear',
            'description': 'Caps, beanies, and hats to complete your look',
            'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fde3830a62f2e4e32b3e515795bd471cf?format=webp&width=600',
            'featured': True,
        },
        {
            'key': 'accessories',
            'label': 'Accessories',
            'description': 'Bags, socks, and essential accessories',
            'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=600',
            'featured': False,
        }
    ]
    
    print("Adding sample categories...")
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            key=cat_data['key'],
            defaults={
                'label': cat_data['label'],
                'description': cat_data['description'],
                'image': cat_data['image'],
                'featured': cat_data['featured'],
            }
        )
        
        if created:
            print(f"✅ Created category: {category.label}")
        else:
            # Update existing category
            category.label = cat_data['label']
            category.description = cat_data['description']
            category.image = cat_data['image']
            category.featured = cat_data['featured']
            category.save()
            print(f"🔄 Updated category: {category.label}")
    
    print(f"\n✅ Successfully processed {len(categories_data)} categories!")
    print(f"Total categories in database: {Category.objects.count()}")
    print(f"Featured categories: {Category.objects.filter(featured=True).count()}")

if __name__ == '__main__':
    add_sample_categories()