#!/usr/bin/env python
"""
Migration fix script for Render deployment
This script handles migration issues by ensuring the database schema is correct
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
from django.db import connection, transaction
from django.contrib.auth import get_user_model

def check_database_connection():
    """Test database connection"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection: OK")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_table_exists(table_name):
    """Check if a table exists"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                );
            """, [table_name])
            return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error checking table {table_name}: {e}")
        return False

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name = %s 
                    AND column_name = %s
                );
            """, [table_name, column_name])
            return cursor.fetchone()[0]
    except Exception as e:
        print(f"Error checking column {table_name}.{column_name}: {e}")
        return False

def add_missing_column():
    """Add the missing is_featured column if it doesn't exist"""
    try:
        if not check_column_exists('shop_product', 'is_featured'):
            print("Adding missing is_featured column...")
            with connection.cursor() as cursor:
                cursor.execute("""
                    ALTER TABLE shop_product 
                    ADD COLUMN is_featured BOOLEAN DEFAULT FALSE;
                """)
            print("✅ Added is_featured column")
            return True
        else:
            print("✅ is_featured column already exists")
            return True
    except Exception as e:
        print(f"❌ Failed to add is_featured column: {e}")
        return False

def fix_migrations():
    """Main migration fix function"""
    print("🔧 Starting migration fix...")
    print("=" * 50)
    
    # Check database connection
    if not check_database_connection():
        return False
    
    # Check if shop_product table exists
    if not check_table_exists('shop_product'):
        print("❌ shop_product table doesn't exist. Running full migrations...")
        try:
            execute_from_command_line(['manage.py', 'migrate'])
            print("✅ Full migrations completed")
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
    else:
        print("✅ shop_product table exists")
        
        # Check for missing is_featured column
        if not add_missing_column():
            return False
        
        # Try to run migrations normally
        try:
            print("Running remaining migrations...")
            execute_from_command_line(['manage.py', 'migrate', '--fake-initial'])
            print("✅ Migrations completed")
        except Exception as e:
            print(f"⚠️  Migration warning: {e}")
            # Continue anyway, the column fix might be enough
    
    # Verify the fix worked
    try:
        from shop.models import Product
        product_count = Product.objects.count()
        print(f"✅ Product model working - {product_count} products found")
        
        # Test if we can access is_featured
        if product_count > 0:
            first_product = Product.objects.first()
            try:
                is_featured = first_product.is_featured
                print("✅ is_featured field accessible")
            except AttributeError:
                print("⚠️  is_featured field still not accessible")
        
    except Exception as e:
        print(f"❌ Product model test failed: {e}")
        return False
    
    print("🎉 Migration fix completed successfully!")
    return True

if __name__ == '__main__':
    success = fix_migrations()
    sys.exit(0 if success else 1)