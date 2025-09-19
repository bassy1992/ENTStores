#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Category, Product
from django.contrib.auth.models import User

def seed_data():
    print("🌱 Seeding database with sample data...")
    
    # Create categories
    categories_data = [
        {'name': 'T-Shirts', 'slug': 't-shirts'},
        {'name': 'Polos', 'slug': 'polos'},
        {'name': 'Hoodies / Crewnecks', 'slug': 'hoodies'},
        {'name': 'Sweatshirts', 'slug': 'sweatshirts'},
        {'name': 'Tracksuits', 'slug': 'tracksuits'},
        {'name': 'Jackets', 'slug': 'jackets'},
        {'name': 'Shorts', 'slug': 'shorts'},
        {'name': 'Headwear', 'slug': 'headwear'},
        {'name': 'Accessories', 'slug': 'accessories'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            key=cat_data['slug'],
            defaults={
                'label': cat_data['name'],
                'description': f"Products in the {cat_data['name']} category",
                'image': None,  # Will be uploaded via admin
                'featured': cat_data['slug'] in ['t-shirts', 'hoodies', 'jackets']
            }
        )
        if created:
            print(f"✅ Created category: {category.label}")
    
    # Create sample products
    products_data = [
        {
            'title': 'Classic White T-Shirt',
            'slug': 'classic-white-t-shirt',
            'description': 'Premium cotton t-shirt with signature ENNC logo. Comfortable fit and durable construction.',
            'price': 2500,  # $25.00
            'category_slug': 't-shirts',
            'is_featured': True,
            'stock_quantity': 100,
            'tags': ['featured', 'bestseller']
        },
        {
            'title': 'Navy Blue Polo',
            'slug': 'navy-blue-polo',
            'description': 'Classic polo shirt in navy blue with embroidered logo. Perfect for smart-casual occasions.',
            'price': 3500,  # $35.00
            'category_slug': 'polos',
            'is_featured': False,
            'stock_quantity': 75,
            'tags': ['new']
        },
        {
            'title': 'Black Hoodie',
            'slug': 'black-hoodie',
            'description': 'Comfortable black hoodie with kangaroo pocket and adjustable drawstring hood.',
            'price': 4500,  # $45.00
            'category_slug': 'hoodies',
            'is_featured': True,
            'stock_quantity': 60,
            'tags': ['featured', 'bestseller']
        },
        {
            'title': 'Athletic Shorts - Navy',
            'slug': 'athletic-shorts-navy',
            'description': 'Lightweight athletic shorts with moisture-wicking fabric and side pockets.',
            'price': 3000,  # $30.00
            'category_slug': 'shorts',
            'is_featured': False,
            'stock_quantity': 80,
            'tags': ['new']
        },
        {
            'title': 'Wool Beanie - Charcoal',
            'slug': 'wool-beanie-charcoal',
            'description': 'Soft merino wool beanie with fold-over cuff and embroidered logo patch.',
            'price': 1500,  # $15.00
            'category_slug': 'headwear',
            'is_featured': False,
            'stock_quantity': 50,
            'tags': ['new']
        },
        {
            'title': 'Track Jacket - Olive',
            'slug': 'track-jacket-olive',
            'description': 'ENNC retro-inspired track jacket in olive tones. Durable construction with branded sleeve tab.',
            'price': 7500,  # $75.00
            'category_slug': 'tracksuits',
            'is_featured': True,
            'stock_quantity': 30,
            'tags': ['featured']
        },
        {
            'title': 'Canvas Duffel Bag',
            'slug': 'canvas-duffel-bag',
            'description': 'Durable canvas duffel with water-repellent coating, metal hardware, and removable shoulder strap.',
            'price': 5500,  # $55.00
            'category_slug': 'accessories',
            'is_featured': False,
            'stock_quantity': 25,
            'tags': ['new']
        },
        {
            'title': 'Bomber Jacket - Black',
            'slug': 'bomber-jacket-black',
            'description': 'Classic bomber jacket with ribbed collar, cuffs, and hem. Water-resistant outer shell.',
            'price': 8900,  # $89.00
            'category_slug': 'jackets',
            'is_featured': True,
            'stock_quantity': 20,
            'tags': ['featured']
        }
    ]
    
    for prod_data in products_data:
        try:
            category = Category.objects.get(key=prod_data['category_slug'])
            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={
                    'title': prod_data['title'],
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'category': category,
                    'is_active': prod_data.get('is_featured', True),  # Use is_active instead of is_featured
                    'stock_quantity': prod_data['stock_quantity'],
                    'image': None  # Will be uploaded via admin
                }
            )
            if created:
                print(f"✅ Created product: {product.title}")
        except Exception as e:
            print(f"❌ Error creating product {prod_data['title']}: {e}")
    
    # Summary
    print(f"\n📊 Database Summary:")
    print(f"Users: {User.objects.count()}")
    print(f"Categories: {Category.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Active Products: {Product.objects.filter(is_active=True).count()}")
    print("\n✅ Database seeding completed!")

if __name__ == '__main__':
    seed_data()