#!/usr/bin/env python3
"""
Local Production Access Script
Access Railway production database from your local machine
"""

import os
import sys
import django

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set settings for local production access (don't set RAILWAY_ENVIRONMENT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
# Don't set RAILWAY_ENVIRONMENT so it uses external DATABASE_URL

# Setup Django
django.setup()

from shop.models import Product, Category, Order, OrderItem
from django.contrib.auth.models import User


def show_stats():
    """Show production database statistics"""
    print("Production Database Statistics (via External URL)")
    print("=" * 50)
    try:
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
        
        print("\nConnection successful!")
        
    except Exception as e:
        print(f"Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your DATABASE_URL environment variable")
        print("2. Ensure it's the external Railway URL (not internal)")
        print("3. Verify the database is accessible from your network")


def list_products():
    """List all products"""
    print("Production Products")
    print("=" * 20)
    
    try:
        products = Product.objects.all()[:10]  # First 10
        for product in products:
            image_type = "URL" if product.image_url else "File" if product.image else "None"
            status = "Active" if product.is_active else "Inactive"
            print(f"[{status}] {product.id}: {product.title}")
            print(f"   Price: ${product.price} | Image: {image_type}")
            if product.image_url:
                print(f"   URL: {product.image_url[:60]}...")
            print()
        
        total = Product.objects.count()
        if total > 10:
            print(f"... and {total - 10} more products")
            
    except Exception as e:
        print(f"Error listing products: {e}")


def add_test_product():
    """Add a test product with URL image"""
    print("Adding test product...")
    
    try:
        # Get or create t-shirts category
        category, created = Category.objects.get_or_create(
            key='t-shirts',
            defaults={
                'label': 'T-Shirts',
                'description': 'Comfortable t-shirts for everyday wear'
            }
        )
        
        # Create test product
        product, created = Product.objects.update_or_create(
            id='test-local-prod',
            defaults={
                'title': 'Test Local Production Product',
                'price': '19.99',
                'description': 'Test product created from local terminal',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop',
                'category': category,
                'stock_quantity': 5,
                'is_active': True,
                'is_featured': False
            }
        )
        
        action = "Created" if created else "Updated"
        print(f"{action} test product: {product.title}")
        print(f"Image URL: {product.image_url}")
        
    except Exception as e:
        print(f"Error adding test product: {e}")


def interactive_shell():
    """Start an interactive Python shell with production database"""
    print("Starting interactive shell with production database...")
    print("Available models: Product, Category, Order, OrderItem, User")
    print("Example commands:")
    print("  Product.objects.all()")
    print("  Category.objects.filter(featured=True)")
    print("  Order.objects.count()")
    print()
    
    # Import everything for convenience
    from django.db.models import Q, Count, Sum
    import datetime
    
    # Start interactive shell
    import code
    code.interact(local=locals())


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Local Production Database Access")
        print("=" * 35)
        print("Usage: python prod_local.py <command>")
        print()
        print("Commands:")
        print("  stats     - Show database statistics")
        print("  products  - List products")
        print("  add-test  - Add a test product")
        print("  shell     - Interactive Python shell")
        print()
        print("Make sure your DATABASE_URL environment variable is set!")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'stats':
        show_stats()
    elif command == 'products':
        list_products()
    elif command == 'add-test':
        add_test_product()
    elif command == 'shell':
        interactive_shell()
    else:
        print(f"Unknown command: {command}")
        print("Use: stats, products, add-test, or shell")


if __name__ == '__main__':
    main()