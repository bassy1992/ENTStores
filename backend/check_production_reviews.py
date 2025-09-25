#!/usr/bin/env python
"""
Check production database for review tables and data
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django with production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Set production environment variables
os.environ['DEBUG'] = 'false'
os.environ['USE_SQLITE'] = 'false'
os.environ['DATABASE_URL'] = 'postgresql://entstore_db_user:m3we2cxnqRNZSMc6B5RK0vDsnku7QAXa@dpg-d36utrmmcj7s73e0q0dg-a/entstore_db'

django.setup()

from django.db import connection
from shop.models import Product, ProductReview

def check_production_reviews():
    """Check production database for review system"""
    
    print("🔍 Checking production database for review system...")
    
    # Check database connection
    print("\n1️⃣ Testing database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"   ✅ Connected to PostgreSQL: {version[0]}")
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
        return
    
    # Check if review tables exist
    print("\n2️⃣ Checking for review tables...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE '%review%'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
        if tables:
            print(f"   ✅ Found review tables:")
            for table in tables:
                print(f"      - {table[0]}")
        else:
            print("   ❌ No review tables found!")
            print("   🔧 Need to run migrations:")
            print("      python manage.py makemigrations shop")
            print("      python manage.py migrate")
            return
            
    except Exception as e:
        print(f"   ❌ Error checking tables: {e}")
        return
    
    # Check products
    print("\n3️⃣ Checking products...")
    try:
        products_count = Product.objects.count()
        print(f"   📦 Found {products_count} products in production")
        
        if products_count > 0:
            sample_products = Product.objects.all()[:3]
            for product in sample_products:
                print(f"      - {product.id}: {product.title}")
        else:
            print("   ⚠️ No products found in production")
            
    except Exception as e:
        print(f"   ❌ Error checking products: {e}")
        return
    
    # Check reviews
    print("\n4️⃣ Checking reviews...")
    try:
        reviews_count = ProductReview.objects.count()
        print(f"   📝 Found {reviews_count} reviews in production")
        
        if reviews_count > 0:
            sample_reviews = ProductReview.objects.all()[:5]
            for review in sample_reviews:
                print(f"      - {review.user_name}: {review.title} ({review.rating}★) - Product: {review.product.title}")
        else:
            print("   ⚠️ No reviews found in production database")
            print("   💡 This explains why the admin shows no reviews")
            
    except Exception as e:
        print(f"   ❌ Error checking reviews: {e}")
        print("   💡 This might mean the ProductReview table doesn't exist")
        return
    
    # Check migrations
    print("\n5️⃣ Checking migrations...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT app, name 
                FROM django_migrations 
                WHERE app = 'shop' 
                ORDER BY applied DESC 
                LIMIT 5;
            """)
            migrations = cursor.fetchall()
            
        if migrations:
            print("   📋 Recent shop migrations:")
            for migration in migrations:
                print(f"      - {migration[1]}")
                
            # Check for review migration specifically
            cursor.execute("""
                SELECT name 
                FROM django_migrations 
                WHERE app = 'shop' 
                AND name LIKE '%review%';
            """)
            review_migrations = cursor.fetchall()
            
            if review_migrations:
                print(f"   ✅ Found review migrations: {[m[0] for m in review_migrations]}")
            else:
                print("   ❌ No review migrations found!")
                print("   🔧 Need to run: python manage.py migrate")
        else:
            print("   ❌ No shop migrations found")
            
    except Exception as e:
        print(f"   ❌ Error checking migrations: {e}")
    
    print("\n🏁 Production database check completed!")

if __name__ == '__main__':
    check_production_reviews()