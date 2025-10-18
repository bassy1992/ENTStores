#!/usr/bin/env python
"""
Deploy production data to Railway PostgreSQL database
This script is designed to run on Railway and populate the database with initial data
"""

import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Category, Product
from decimal import Decimal


def create_categories():
    """Create sample categories"""
    categories_data = [
        {
            'key': 't-shirts',
            'label': 'T-Shirts',
            'description': 'Comfortable and stylish t-shirts for everyday wear',
            'featured': True
        },
        {
            'key': 'hoodies',
            'label': 'Hoodies / Crewnecks',
            'description': 'Cozy hoodies and crewnecks for cooler weather',
            'featured': True
        },
        {
            'key': 'polos',
            'label': 'Polos',
            'description': 'Classic polo shirts for a smart casual look',
            'featured': False
        },
        {
            'key': 'tracksuits',
            'label': 'Tracksuits',
            'description': 'Complete tracksuit sets for comfort and style',
            'featured': True
        },
        {
            'key': 'jackets',
            'label': 'Jackets',
            'description': 'Stylish jackets for all seasons',
            'featured': False
        },
        {
            'key': 'shorts',
            'label': 'Shorts',
            'description': 'Comfortable shorts for warm weather',
            'featured': False
        },
        {
            'key': 'accessories',
            'label': 'Accessories',
            'description': 'Complete your look with our accessories',
            'featured': False
        }
    ]
    
    created_count = 0
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            key=cat_data['key'],
            defaults=cat_data
        )
        if created:
            created_count += 1
            print(f"✅ Created category: {category.label}")
        else:
            print(f"⏭️  Category exists: {category.label}")
    
    return created_count


def create_products():
    """Create sample products"""
    products_data = [
        {
            'id': 'ent-tshirt-black-001',
            'title': 'ENNC Classic Tee — Black',
            'slug': 'ennc-classic-tee-black-001',
            'price': Decimal('25.00'),
            'description': 'Premium quality black t-shirt with ENNC branding. Made from 100% cotton for maximum comfort.',
            'category_key': 't-shirts',
            'stock_quantity': 50,
            'is_featured': True,
            'shipping_cost': Decimal('9.99'),
            'image_url': 'https://via.placeholder.com/400x400/000000/ffffff?text=ENNC+Black+Tee'
        },
        {
            'id': 'ent-tshirt-white-001',
            'title': 'ENNC Classic Tee — White',
            'slug': 'ennc-classic-tee-white-001',
            'price': Decimal('25.00'),
            'description': 'Premium quality white t-shirt with ENNC branding. Made from 100% cotton for maximum comfort.',
            'category_key': 't-shirts',
            'stock_quantity': 45,
            'is_featured': True,
            'shipping_cost': Decimal('9.99'),
            'image_url': 'https://via.placeholder.com/400x400/ffffff/000000?text=ENNC+White+Tee'
        },
        {
            'id': 'ent-hoodie-grey-001',
            'title': 'ENNC Essential Hoodie — Grey',
            'slug': 'ennc-essential-hoodie-grey-001',
            'price': Decimal('55.00'),
            'description': 'Comfortable grey hoodie with premium fleece lining. Perfect for casual wear and layering.',
            'category_key': 'hoodies',
            'stock_quantity': 30,
            'is_featured': True,
            'shipping_cost': Decimal('12.99'),
            'image_url': 'https://via.placeholder.com/400x400/808080/ffffff?text=ENNC+Grey+Hoodie'
        },
        {
            'id': 'ent-hoodie-black-001',
            'title': 'ENNC Essential Hoodie — Black',
            'slug': 'ennc-essential-hoodie-black-001',
            'price': Decimal('55.00'),
            'description': 'Comfortable black hoodie with premium fleece lining. Perfect for casual wear and layering.',
            'category_key': 'hoodies',
            'stock_quantity': 35,
            'is_featured': True,
            'shipping_cost': Decimal('12.99'),
            'image_url': 'https://via.placeholder.com/400x400/000000/ffffff?text=ENNC+Black+Hoodie'
        },
        {
            'id': 'ent-polo-navy-001',
            'title': 'ENNC Classic Polo — Navy',
            'slug': 'ennc-classic-polo-navy-001',
            'price': Decimal('35.00'),
            'description': 'Classic navy polo shirt with ENNC embroidery. Perfect for smart casual occasions.',
            'category_key': 'polos',
            'stock_quantity': 25,
            'is_featured': False,
            'shipping_cost': Decimal('9.99'),
            'image_url': 'https://via.placeholder.com/400x400/000080/ffffff?text=ENNC+Navy+Polo'
        },
        {
            'id': 'ent-tracksuit-black-001',
            'title': 'ENNC Tracksuit Set — Black',
            'slug': 'ennc-tracksuit-set-black-001',
            'price': Decimal('85.00'),
            'description': 'Complete tracksuit set including hoodie and joggers. Premium comfort for active lifestyle.',
            'category_key': 'tracksuits',
            'stock_quantity': 20,
            'is_featured': True,
            'shipping_cost': Decimal('15.99'),
            'image_url': 'https://via.placeholder.com/400x400/000000/ffffff?text=ENNC+Tracksuit'
        },
        {
            'id': 'ent-jacket-blue-001',
            'title': 'ENNC Windbreaker — Blue',
            'slug': 'ennc-windbreaker-blue-001',
            'price': Decimal('65.00'),
            'description': 'Lightweight windbreaker jacket perfect for outdoor activities. Water-resistant material.',
            'category_key': 'jackets',
            'stock_quantity': 15,
            'is_featured': False,
            'shipping_cost': Decimal('12.99'),
            'image_url': 'https://via.placeholder.com/400x400/0000ff/ffffff?text=ENNC+Windbreaker'
        },
        {
            'id': 'ent-shorts-grey-001',
            'title': 'ENNC Athletic Shorts — Grey',
            'slug': 'ennc-athletic-shorts-grey-001',
            'price': Decimal('30.00'),
            'description': 'Comfortable athletic shorts with moisture-wicking fabric. Perfect for workouts and casual wear.',
            'category_key': 'shorts',
            'stock_quantity': 40,
            'is_featured': False,
            'shipping_cost': Decimal('8.99'),
            'image_url': 'https://via.placeholder.com/400x400/808080/ffffff?text=ENNC+Shorts'
        }
    ]
    
    created_count = 0
    for prod_data in products_data:
        category_key = prod_data.pop('category_key')
        
        try:
            category = Category.objects.get(key=category_key)
            prod_data['category'] = category
            
            product, created = Product.objects.get_or_create(
                id=prod_data['id'],
                defaults=prod_data
            )
            
            if created:
                created_count += 1
                print(f"✅ Created product: {product.title}")
            else:
                print(f"⏭️  Product exists: {product.title}")
                
        except Category.DoesNotExist:
            print(f"❌ Category '{category_key}' not found for product {prod_data['id']}")
    
    return created_count


def main():
    """Main function to populate the database"""
    print("🚀 Deploying production data...")
    
    # Check if we're in production (Railway environment)
    is_production = os.getenv('RAILWAY_ENVIRONMENT') is not None
    print(f"Environment: {'Production (Railway)' if is_production else 'Development'}")
    
    print(f"📊 Current counts:")
    print(f"  Categories: {Category.objects.count()}")
    print(f"  Products: {Product.objects.count()}")
    
    # Only proceed if database is empty or nearly empty
    if Category.objects.count() == 0 or Product.objects.count() == 0:
        print("\n📁 Creating categories...")
        categories_created = create_categories()
        
        print("\n🛍️  Creating products...")
        products_created = create_products()
        
        print(f"\n📊 Final counts:")
        print(f"  Categories: {Category.objects.count()}")
        print(f"  Products: {Product.objects.count()}")
        
        print(f"\n✅ Database population completed!")
        print(f"  Categories created: {categories_created}")
        print(f"  Products created: {products_created}")
    else:
        print("\n⏭️  Database already has data, skipping population")
        print("   Use --force flag if you want to add data anyway")


if __name__ == "__main__":
    main()