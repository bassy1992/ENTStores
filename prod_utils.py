#!/usr/bin/env python3
"""
Production Database Utilities
Common tasks for production database management
"""

import os
import sys
import django

# Setup
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
os.environ.setdefault('RAILWAY_ENVIRONMENT', 'production')

django.setup()

from shop.models import Product, Category, Order, OrderItem
from django.contrib.auth.models import User


def show_stats():
    """Show production database statistics"""
    print("Production Database Statistics")
    print("=" * 35)
    print(f"Products: {Product.objects.count()}")
    print(f"Categories: {Category.objects.count()}")
    print(f"Orders: {Order.objects.count()}")
    print(f"Users: {User.objects.count()}")
    
    # Products with URL images
    url_products = Product.objects.filter(image_url__isnull=False).exclude(image_url='')
    print(f"Products with URL images: {url_products.count()}")
    
    # Featured products
    featured = Product.objects.filter(is_featured=True)
    print(f"Featured products: {featured.count()}")


def list_products():
    """List all products"""
    print("Production Products")
    print("=" * 25)
    
    products = Product.objects.all()[:20]  # First 20
    for product in products:
        image_type = "URL" if product.image_url else "File" if product.image else "None"
        status = "Active" if product.is_active else "Inactive"
        print(f"{status} {product.id}: {product.title} (${product.price}) [{image_type}]")
    
    if Product.objects.count() > 20:
        print(f"... and {Product.objects.count() - 20} more products")


def list_orders():
    """List recent orders"""
    print("Recent Orders")
    print("=" * 15)
    
    orders = Order.objects.all()[:10]  # Last 10
    for order in orders:
        print(f"{order.id}: {order.customer_name} - ${order.total} ({order.status})")


def backup_data():
    """Create a data backup"""
    print("Creating data backup...")
    
    from django.core.management import call_command
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"production_backup_{timestamp}.json"
    
    try:
        call_command('dumpdata', '--natural-foreign', '--natural-primary', 
                    '--exclude=contenttypes', '--exclude=auth.permission',
                    '--output='+filename)
        print(f"Backup created: {filename}")
    except Exception as e:
        print(f"Backup failed: {e}")


def main():
    """Main utility function"""
    if len(sys.argv) < 2:
        print("Production Database Utilities")
        print("=" * 35)
        print("Usage: python prod_utils.py <command>")
        print("")
        print("Commands:")
        print("  stats     - Show database statistics")
        print("  products  - List products")
        print("  orders    - List recent orders")
        print("  backup    - Create data backup")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'stats':
        show_stats()
    elif command == 'products':
        list_products()
    elif command == 'orders':
        list_orders()
    elif command == 'backup':
        backup_data()
    else:
        print(f"Unknown command: {command}")


if __name__ == '__main__':
    main()