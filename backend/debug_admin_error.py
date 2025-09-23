#!/usr/bin/env python
"""
Debug script to identify admin errors for OrderItem model
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db import connection
from shop.models import OrderItem, Order, Product, ProductVariant
from django.contrib.admin.sites import site
from shop.admin import OrderItemAdmin

def test_database_connection():
    """Test basic database connectivity"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_orderitem_model():
    """Test OrderItem model operations"""
    try:
        # Test basic query
        count = OrderItem.objects.count()
        print(f"✅ OrderItem count: {count}")
        
        # Test with select_related (what admin uses)
        items = OrderItem.objects.select_related('order', 'product', 'product_variant').all()[:5]
        print(f"✅ OrderItem query with relations successful: {len(list(items))} items")
        
        # Test individual fields
        for item in items:
            print(f"   - Order: {item.order_id}, Product: {item.product.title}")
            if hasattr(item, 'product_variant') and item.product_variant:
                print(f"     Variant: {item.product_variant}")
            if item.selected_size or item.selected_color:
                print(f"     Size: {item.selected_size}, Color: {item.selected_color}")
        
        return True
    except Exception as e:
        print(f"❌ OrderItem model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_queryset():
    """Test the admin queryset that's causing issues"""
    try:
        admin_instance = OrderItemAdmin(OrderItem, site)
        queryset = admin_instance.get_queryset(None)
        
        # Try to evaluate the queryset
        items = list(queryset[:5])
        print(f"✅ Admin queryset successful: {len(items)} items")
        
        # Test admin list display methods
        for item in items:
            try:
                variant_info = admin_instance.variant_info_display(item)
                print(f"   - Variant info: {variant_info}")
            except Exception as e:
                print(f"   ❌ Variant info display error: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Admin queryset test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_missing_migrations():
    """Check if there are any unapplied migrations"""
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.showmigrations import Command
        
        print("\n📋 Checking migration status...")
        execute_from_command_line(['manage.py', 'showmigrations', 'shop'])
        return True
    except Exception as e:
        print(f"❌ Migration check failed: {e}")
        return False

def main():
    print("🔍 Debugging OrderItem Admin Error")
    print("=" * 50)
    
    # Test database connection
    if not test_database_connection():
        return
    
    # Check migrations
    check_missing_migrations()
    
    # Test model operations
    print("\n🧪 Testing OrderItem model...")
    if not test_orderitem_model():
        return
    
    # Test admin functionality
    print("\n👨‍💼 Testing Admin functionality...")
    if not test_admin_queryset():
        return
    
    print("\n✅ All tests passed! The admin should be working.")
    print("If you're still seeing 500 errors, check the server logs for more details.")

if __name__ == '__main__':
    main()