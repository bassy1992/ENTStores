from django.core.management.base import BaseCommand
from django.db import transaction
from shop.models import Category, Product, Order, OrderItem
import sqlite3
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Migrate data from SQLite to current database (PostgreSQL)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sqlite-path',
            type=str,
            default='db.sqlite3',
            help='Path to SQLite database file'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be migrated without actually doing it'
        )

    def handle(self, *args, **options):
        sqlite_path = options['sqlite_path']
        dry_run = options['dry_run']
        
        # Get absolute path to SQLite file
        if not os.path.isabs(sqlite_path):
            sqlite_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', sqlite_path)
        
        if not os.path.exists(sqlite_path):
            self.stdout.write(
                self.style.ERROR(f'SQLite database not found at: {sqlite_path}')
            )
            return
        
        self.stdout.write(f'Reading from SQLite: {sqlite_path}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        try:
            with transaction.atomic():
                self.migrate_data(sqlite_path, dry_run)
                if dry_run:
                    raise Exception("Dry run - rolling back")
        except Exception as e:
            if "Dry run" in str(e):
                self.stdout.write(self.style.SUCCESS('Dry run completed'))
            else:
                self.stdout.write(self.style.ERROR(f'Migration failed: {e}'))
                raise

    def migrate_data(self, sqlite_path, dry_run):
        # Connect to SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row  # Access columns by name
        cursor = sqlite_conn.cursor()
        
        try:
            # Get current counts
            current_categories = Category.objects.count()
            current_products = Product.objects.count()
            current_orders = Order.objects.count()
            
            self.stdout.write(f'Current PostgreSQL counts:')
            self.stdout.write(f'  Categories: {current_categories}')
            self.stdout.write(f'  Products: {current_products}')
            self.stdout.write(f'  Orders: {current_orders}')
            
            # Migrate Categories
            self.stdout.write('\n📁 Migrating Categories...')
            cursor.execute("SELECT * FROM shop_category")
            sqlite_categories = cursor.fetchall()
            
            existing_category_keys = set(Category.objects.values_list('key', flat=True))
            categories_added = 0
            
            for row in sqlite_categories:
                # Handle both old and new schema
                if 'key' in row.keys():
                    # New schema with key field
                    key = row['key']
                    label = row['label']
                    description = row['description']
                    image = row['image']
                else:
                    # Old schema - map name to key
                    name = row['name']
                    key = name.lower().replace(' ', '-').replace('/', '-')
                    label = name
                    description = row['description']
                    image = row['image']
                
                if key not in existing_category_keys:
                    if not dry_run:
                        Category.objects.create(
                            key=key,
                            label=label,
                            description=description,
                            image=image
                        )
                    categories_added += 1
                    self.stdout.write(f'  ✅ Would add category: {label} (key: {key})')
                else:
                    self.stdout.write(f'  ⏭️  Category exists: {label} (key: {key})')
            
            # Migrate Products
            self.stdout.write('\n🛍️  Migrating Products...')
            cursor.execute("SELECT * FROM shop_product")
            sqlite_products = cursor.fetchall()
            
            existing_product_ids = set(Product.objects.values_list('id', flat=True))
            products_added = 0
            
            for row in sqlite_products:
                product_id = row['id']
                
                if product_id not in existing_product_ids:
                    # Handle both old and new schema
                    columns = [col[0] for col in cursor.description]
                    
                    if 'title' in columns:
                        # New schema
                        title = row['title']
                        slug = row['slug'] if 'slug' in columns else ''
                        price = row['price']
                        description = row['description']
                        image = row['image']
                        image_url = row['image_url'] if 'image_url' in columns else ''
                        category_key = row['category_id'] if 'category_id' in columns else ''
                        stock_quantity = row['stock_quantity']
                        is_featured = row['is_featured'] if 'is_featured' in columns else False
                        shipping_cost = row['shipping_cost'] if 'shipping_cost' in columns else 9.99
                    else:
                        # Old schema - map fields
                        title = row['name']
                        slug = ''
                        price = row['price']
                        description = row['description']
                        image = row['image']
                        image_url = ''
                        category_key = row['category_id'] if 'category_id' in columns else ''
                        stock_quantity = row['stock_quantity']
                        is_featured = row['is_featured'] if 'is_featured' in columns else False
                        shipping_cost = row['shipping_cost'] if 'shipping_cost' in columns else 9.99
                    
                    # Find category by key or create mapping
                    try:
                        if category_key:
                            category = Category.objects.get(key=category_key)
                        else:
                            category = Category.objects.first()  # Fallback
                    except Category.DoesNotExist:
                        # Create a default category if needed
                        category, created = Category.objects.get_or_create(
                            key='general',
                            defaults={
                                'label': 'General',
                                'description': 'General products'
                            }
                        )
                    
                    if not dry_run:
                        Product.objects.create(
                            id=product_id,
                            title=title,
                            slug=slug or title.lower().replace(' ', '-'),
                            price=price,
                            description=description,
                            image=image,
                            image_url=image_url,
                            category=category,
                            stock_quantity=stock_quantity,
                            is_featured=is_featured,
                            shipping_cost=shipping_cost
                        )
                    products_added += 1
                    self.stdout.write(f'  ✅ Would add product: {title} (ID: {product_id})')
                else:
                    self.stdout.write(f'  ⏭️  Product exists: {product_id}')
            
            # Migrate Orders
            self.stdout.write('\n📦 Migrating Orders...')
            cursor.execute("SELECT * FROM shop_order")
            sqlite_orders = cursor.fetchall()
            
            existing_order_ids = set(Order.objects.values_list('id', flat=True))
            orders_added = 0
            
            for row in sqlite_orders:
                order_id = row['id']
                
                if order_id not in existing_order_ids:
                    # Handle both old and new schema
                    order_columns = [col[0] for col in cursor.description]
                    
                    if 'customer_email' in order_columns:
                        # New schema
                        customer_email = row['customer_email']
                        customer_name = row['customer_name']
                        shipping_address = row['shipping_address'] if 'shipping_address' in order_columns else (row['address'] if 'address' in order_columns else '')
                        shipping_city = row['shipping_city'] if 'shipping_city' in order_columns else (row['city'] if 'city' in order_columns else '')
                        shipping_country = row['shipping_country'] if 'shipping_country' in order_columns else (row['country'] if 'country' in order_columns else '')
                        subtotal = row['subtotal'] if 'subtotal' in order_columns else (row['total_amount'] if 'total_amount' in order_columns else 0)
                        total = row['total'] if 'total' in order_columns else (row['total_amount'] if 'total_amount' in order_columns else 0)
                        tracking_number = row['tracking_number'] if 'tracking_number' in order_columns else ''
                        payment_method = row['payment_method'] if 'payment_method' in order_columns else 'unknown'
                        created_at = row['created_at'] if 'created_at' in order_columns else ''
                    else:
                        # Old schema - map fields
                        customer_email = row['customer_email']
                        customer_name = row['customer_name']
                        shipping_address = row['address'] if 'address' in order_columns else ''
                        shipping_city = row['city'] if 'city' in order_columns else ''
                        shipping_country = row['country'] if 'country' in order_columns else ''
                        subtotal = row['total_amount'] if 'total_amount' in order_columns else 0
                        total = row['total_amount'] if 'total_amount' in order_columns else 0
                        tracking_number = row['tracking_number'] if 'tracking_number' in order_columns else ''
                        payment_method = 'unknown'
                        created_at = row['created_at'] if 'created_at' in order_columns else ''
                    
                    if not dry_run:
                        Order.objects.create(
                            id=order_id,
                            customer_email=customer_email,
                            customer_name=customer_name,
                            shipping_address=shipping_address,
                            shipping_city=shipping_city,
                            shipping_country=shipping_country,
                            subtotal=subtotal,
                            total=total,
                            tracking_number=tracking_number,
                            payment_method=payment_method
                        )
                    orders_added += 1
                    self.stdout.write(f'  ✅ Would add order: {customer_name} - ${total} (ID: {order_id})')
                    
                    # Migrate Order Items
                    cursor.execute("SELECT * FROM shop_orderitem WHERE order_id = ?", (order_id,))
                    order_items = cursor.fetchall()
                    
                    for item_row in order_items:
                        product_id = item_row['product_id']
                        quantity = item_row['quantity']
                        item_columns = [col[0] for col in cursor.description]
                        unit_price = item_row['price'] if 'price' in item_columns else (item_row['unit_price'] if 'unit_price' in item_columns else 0)
                        
                        # Check if product exists
                        try:
                            product = Product.objects.get(id=product_id)
                            if not dry_run:
                                OrderItem.objects.create(
                                    order_id=order_id,
                                    product=product,
                                    quantity=quantity,
                                    unit_price=unit_price,
                                    total_price=quantity * unit_price
                                )
                            self.stdout.write(f'    ➕ Would add order item: {product_id} x{quantity}')
                        except Product.DoesNotExist:
                            self.stdout.write(f'    ⚠️  Product {product_id} not found for order item')
                else:
                    self.stdout.write(f'  ⏭️  Order exists: {order_id}')
            
            # Summary
            self.stdout.write(f'\n📊 Migration Summary:')
            self.stdout.write(f'  Categories to add: {categories_added}')
            self.stdout.write(f'  Products to add: {products_added}')
            self.stdout.write(f'  Orders to add: {orders_added}')
            
            if not dry_run:
                # Final counts
                final_categories = Category.objects.count()
                final_products = Product.objects.count()
                final_orders = Order.objects.count()
                
                self.stdout.write(f'\n📊 Final PostgreSQL counts:')
                self.stdout.write(f'  Categories: {final_categories}')
                self.stdout.write(f'  Products: {final_products}')
                self.stdout.write(f'  Orders: {final_orders}')
                
                self.stdout.write(self.style.SUCCESS('\n✅ Migration completed successfully!'))
            
        finally:
            sqlite_conn.close()