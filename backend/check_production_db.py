#!/usr/bin/env python
"""
Check production database status and run migrations if needed
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Force production settings
os.environ['DEBUG'] = 'false'
os.environ['RENDER'] = 'true'

django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from shop.models import OrderItem, Order, Product

def check_database_connection():
    """Check if we can connect to the production database"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"✅ Connected to PostgreSQL: {version}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_migrations():
    """Check migration status"""
    try:
        print("\n📋 Checking migration status...")
        execute_from_command_line(['manage.py', 'showmigrations'])
        return True
    except Exception as e:
        print(f"❌ Migration check failed: {e}")
        return False

def run_migrations():
    """Run any pending migrations"""
    try:
        print("\n🔄 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def test_orderitem_access():
    """Test OrderItem model access"""
    try:
        count = OrderItem.objects.count()
        print(f"✅ OrderItem count: {count}")
        
        # Test the problematic admin query
        items = OrderItem.objects.select_related('order', 'product', 'product_variant').all()[:5]
        print(f"✅ OrderItem admin query successful: {len(list(items))} items")
        return True
    except Exception as e:
        print(f"❌ OrderItem access failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🔍 Checking Production Database Status")
    print("=" * 50)
    
    # Check database connection
    if not check_database_connection():
        print("Cannot proceed without database connection")
        return
    
    # Check migrations
    check_migrations()
    
    # Run migrations if needed
    run_migrations()
    
    # Test OrderItem access
    print("\n🧪 Testing OrderItem access...")
    test_orderitem_access()
    
    print("\n✅ Production database check complete!")

if __name__ == '__main__':
    main()