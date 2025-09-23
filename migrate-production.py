#!/usr/bin/env python
"""
Production Database Migration Script for Render
This script helps migrate your local data to the production PostgreSQL database
"""

import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from shop.models import Category, Product

def main():
    print("🚀 ENTstore Production Database Migration")
    print("=" * 50)
    
    # Check if we're using PostgreSQL
    from django.conf import settings
    db_engine = settings.DATABASES['default']['ENGINE']
    
    if 'postgresql' not in db_engine:
        print("❌ Not using PostgreSQL database")
        print("   Make sure DATABASE_URL is set and USE_SQLITE=false")
        return
    
    print(f"✅ Connected to PostgreSQL database")
    print(f"   Database: {settings.DATABASES['default']['NAME']}")
    print(f"   Host: {settings.DATABASES['default']['HOST']}")
    
    # Run migrations
    print("\n📋 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return
    
    # Create superuser if it doesn't exist
    print("\n👤 Setting up admin user...")
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        try:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='Enontinoclothing@gmail.com',
                password='admin123'  # Change this in production!
            )
            print("✅ Admin user created successfully")
            print("   Username: admin")
            print("   Password: admin123")
            print("   ⚠️  IMPORTANT: Change the password after first login!")
        except Exception as e:
            print(f"❌ Failed to create admin user: {e}")
    else:
        print("✅ Admin user already exists")
    
    # Check existing data
    print("\n📊 Checking existing data...")
    
    categories_count = Category.objects.count()
    products_count = Product.objects.count()
    users_count = User.objects.count()
    
    print(f"   Categories: {categories_count}")
    print(f"   Products: {products_count}")
    print(f"   Users: {users_count}")
    
    if categories_count == 0:
        print("\n📦 Creating sample categories...")
        try:
            # Create sample categories
            categories = [
                {'name': 'T-Shirts', 'description': 'Comfortable cotton t-shirts'},
                {'name': 'Hoodies', 'description': 'Warm and stylish hoodies'},
                {'name': 'Accessories', 'description': 'Fashion accessories'},
            ]
            
            for cat_data in categories:
                category, created = Category.objects.get_or_create(
                    name=cat_data['name'],
                    defaults={'description': cat_data['description']}
                )
                if created:
                    print(f"   ✅ Created category: {category.name}")
                else:
                    print(f"   ℹ️  Category exists: {category.name}")
                    
        except Exception as e:
            print(f"❌ Failed to create categories: {e}")
    
    print("\n🎉 Production database setup completed!")
    print("\n📋 Next steps:")
    print("1. Deploy to Render with the updated configuration")
    print("2. Test the API endpoints:")
    print("   - https://your-app.onrender.com/api/health/")
    print("   - https://your-app.onrender.com/api/shop/categories/")
    print("   - https://your-app.onrender.com/admin/")
    print("3. Change the admin password after first login")
    print("4. Upload your product images and data through the admin panel")

if __name__ == '__main__':
    main()