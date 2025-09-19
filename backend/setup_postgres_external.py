#!/usr/bin/env python
import os
import django
from django.conf import settings

# Set the external DATABASE_URL
os.environ['DATABASE_URL'] = 'postgresql://postgres:cOmslSkNXoXbZzpnezpTPustrmuDgAoN@ballast.proxy.rlwy.net:23564/railway'

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from shop.models import Category, Product

def setup_database():
    print("🔧 Setting up PostgreSQL database with external connection...")
    print(f"🔗 Using: {os.environ.get('DATABASE_URL')[:50]}...")
    
    try:
        # Run migrations
        print("📦 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Create superuser
        print("👤 Creating superuser...")
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='password123'
            )
            print("✅ Superuser created: admin / password123")
        else:
            print("✅ Superuser already exists")
        
        # Create categories
        print("📂 Creating categories...")
        categories_data = [
            {'key': 't-shirts', 'label': 'T-Shirts'},
            {'key': 'polos', 'label': 'Polos'},
            {'key': 'hoodies', 'label': 'Hoodies / Crewnecks'},
            {'key': 'sweatshirts', 'label': 'Sweatshirts'},
            {'key': 'tracksuits', 'label': 'Tracksuits'},
            {'key': 'jackets', 'label': 'Jackets'},
            {'key': 'shorts', 'label': 'Shorts'},
            {'key': 'headwear', 'label': 'Headwear'},
            {'key': 'accessories', 'label': 'Accessories'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                key=cat_data['key'],
                defaults={
                    'label': cat_data['label'],
                    'description': f"Products in the {cat_data['label']} category",
                    'featured': cat_data['key'] in ['t-shirts', 'hoodies', 'jackets']
                }
            )
            if created:
                print(f"✅ Created category: {category.label}")
        
        print("✅ PostgreSQL database setup completed!")
        print(f"📊 Users: {User.objects.count()}")
        print(f"📊 Categories: {Category.objects.count()}")
        print(f"📊 Products: {Product.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    setup_database()