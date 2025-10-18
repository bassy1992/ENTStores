#!/usr/bin/env python3
"""
Production Management Script (Local Access)
Comprehensive production database management from local terminal
"""

import os
import sys
import django

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set settings for local production access
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Setup Django
django.setup()

from shop.models import Product, Category, Order, OrderItem
from django.contrib.auth.models import User
from django.core.management import call_command


def run_migration():
    """Run database migrations"""
    print("Running migrations on production database...")
    try:
        call_command('migrate')
        print("Migrations completed successfully!")
    except Exception as e:
        print(f"Migration failed: {e}")


def create_superuser():
    """Create a superuser"""
    print("Creating superuser...")
    try:
        call_command('createsuperuser')
    except Exception as e:
        print(f"Error creating superuser: {e}")


def collect_static():
    """Collect static files"""
    print("Collecting static files...")
    try:
        call_command('collectstatic', '--noinput')
        print("Static files collected successfully!")
    except Exception as e:
        print(f"Error collecting static files: {e}")


def backup_database():
    """Create database backup"""
    print("Creating database backup...")
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"production_backup_{timestamp}.json"
    
    try:
        call_command('dumpdata', 
                    '--natural-foreign', 
                    '--natural-primary',
                    '--exclude=contenttypes', 
                    '--exclude=auth.permission',
                    '--exclude=sessions',
                    '--output=' + filename)
        print(f"Backup created: {filename}")
    except Exception as e:
        print(f"Backup failed: {e}")


def load_sample_data():
    """Load sample products with URL images"""
    print("Loading sample products with URL images...")
    
    sample_products = [
        {
            "id": "ent-premium-tshirt",
            "title": "ENT Premium T-Shirt",
            "price": "29.99",
            "description": "High-quality cotton t-shirt with premium ENT branding.",
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
            "category": "t-shirts",
            "stock_quantity": 100,
            "is_featured": True
        },
        {
            "id": "ent-comfort-hoodie",
            "title": "ENT Comfort Hoodie",
            "price": "69.99",
            "description": "Ultra-comfortable hoodie perfect for any season.",
            "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop",
            "category": "hoodies",
            "stock_quantity": 50,
            "is_featured": True
        }
    ]
    
    success_count = 0
    for product_data in sample_products:
        try:
            category, _ = Category.objects.get_or_create(
                key=product_data['category'],
                defaults={
                    'label': product_data['category'].replace('-', ' ').title(),
                    'description': f'{product_data["category"].replace("-", " ").title()} collection'
                }
            )
            
            product, created = Product.objects.update_or_create(
                id=product_data['id'],
                defaults={
                    'title': product_data['title'],
                    'price': product_data['price'],
                    'description': product_data['description'],
                    'image_url': product_data['image_url'],
                    'category': category,
                    'stock_quantity': product_data['stock_quantity'],
                    'is_featured': product_data['is_featured'],
                    'is_active': True
                }
            )
            
            action = "Created" if created else "Updated"
            print(f"  {action}: {product.title}")
            success_count += 1
            
        except Exception as e:
            print(f"  Error with {product_data['id']}: {e}")
    
    print(f"Successfully processed {success_count} products")


def update_product_images():
    """Update existing products to use URL images"""
    print("Updating products to use URL images...")
    
    # Map existing products to image URLs
    image_updates = {
        'ennc-essential-hoodie-black': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop&crop=center',
        'ennc-essential-hoodie-grey': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop&crop=center',
        'ennc-classic-tee-white': 'https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&h=400&fit=crop&crop=center',
        'ennc-classic-tee-black': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center'
    }
    
    updated_count = 0
    for product_id, image_url in image_updates.items():
        try:
            product = Product.objects.get(id=product_id)
            product.image_url = image_url
            product.save()
            print(f"  Updated: {product.title}")
            updated_count += 1
        except Product.DoesNotExist:
            print(f"  Product not found: {product_id}")
        except Exception as e:
            print(f"  Error updating {product_id}: {e}")
    
    print(f"Updated {updated_count} products with URL images")


def show_database_info():
    """Show detailed database information"""
    print("Production Database Information")
    print("=" * 35)
    
    try:
        from django.db import connection
        
        # Database info
        db_settings = connection.settings_dict
        print(f"Database: {db_settings['NAME']}")
        print(f"Host: {db_settings['HOST']}")
        print(f"Port: {db_settings['PORT']}")
        print(f"Engine: {db_settings['ENGINE']}")
        
        print("\nTable Counts:")
        print(f"  Products: {Product.objects.count()}")
        print(f"  Categories: {Category.objects.count()}")
        print(f"  Orders: {Order.objects.count()}")
        print(f"  Order Items: {OrderItem.objects.count()}")
        print(f"  Users: {User.objects.count()}")
        
        # Image statistics
        products_with_files = Product.objects.filter(image__isnull=False).exclude(image='')
        products_with_urls = Product.objects.filter(image_url__isnull=False).exclude(image_url='')
        from django.db import models
        products_no_image = Product.objects.filter(
            (models.Q(image__isnull=True) | models.Q(image='')) &
            (models.Q(image_url__isnull=True) | models.Q(image_url=''))
        )
        
        print(f"\nImage Statistics:")
        print(f"  Products with file images: {products_with_files.count()}")
        print(f"  Products with URL images: {products_with_urls.count()}")
        print(f"  Products without images: {products_no_image.count()}")
        
        # Recent activity
        recent_orders = Order.objects.order_by('-created_at')[:5]
        print(f"\nRecent Orders:")
        for order in recent_orders:
            print(f"  {order.id}: ${order.total} - {order.status} ({order.created_at.strftime('%Y-%m-%d')})")
        
    except Exception as e:
        print(f"Error getting database info: {e}")


def interactive_django_shell():
    """Start Django shell with production database"""
    print("Starting Django shell with production database...")
    print("Pre-loaded models: Product, Category, Order, OrderItem, User")
    print("Example: Product.objects.filter(is_featured=True)")
    
    try:
        call_command('shell')
    except Exception as e:
        print(f"Error starting shell: {e}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Production Database Management")
        print("=" * 35)
        print("Usage: python prod_manage_local.py <command>")
        print()
        print("Database Commands:")
        print("  info          - Show database information")
        print("  migrate       - Run migrations")
        print("  backup        - Create database backup")
        print("  shell         - Django shell")
        print()
        print("User Management:")
        print("  createsuperuser - Create admin user")
        print()
        print("Product Management:")
        print("  load-samples    - Load sample products")
        print("  update-images   - Update existing products with URL images")
        print()
        print("Static Files:")
        print("  collectstatic   - Collect static files")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'info':
        show_database_info()
    elif command == 'migrate':
        run_migration()
    elif command == 'backup':
        backup_database()
    elif command == 'shell':
        interactive_django_shell()
    elif command == 'createsuperuser':
        create_superuser()
    elif command == 'load-samples':
        load_sample_data()
    elif command == 'update-images':
        update_product_images()
    elif command == 'collectstatic':
        collect_static()
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments to see available commands")


if __name__ == '__main__':
    main()