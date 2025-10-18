#!/usr/bin/env python
"""
Migrate data from SQLite to PostgreSQL Railway database
This script will copy missing data from your local SQLite database to Railway PostgreSQL
"""

import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).resolve().parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

import sqlite3
import psycopg
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_postgres_connection():
    """Get PostgreSQL connection using Railway credentials"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL not found in environment variables")
    
    return psycopg.connect(database_url)

def get_sqlite_connection():
    """Get SQLite connection"""
    sqlite_path = backend_dir / 'db.sqlite3'
    if not sqlite_path.exists():
        raise FileNotFoundError(f"SQLite database not found at {sqlite_path}")
    
    return sqlite3.connect(str(sqlite_path))

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    print("🔄 Starting data migration from SQLite to PostgreSQL...")
    
    # Connect to both databases
    sqlite_conn = get_sqlite_connection()
    postgres_conn = get_postgres_connection()
    
    sqlite_cursor = sqlite_conn.cursor()
    postgres_cursor = postgres_conn.cursor()
    
    try:
        # Get current max IDs from PostgreSQL to avoid conflicts
        postgres_cursor.execute("SELECT COALESCE(MAX(CAST(id AS INTEGER)), 0) FROM shop_category")
        max_category_id = postgres_cursor.fetchone()[0]
        
        postgres_cursor.execute("SELECT COALESCE(MAX(CAST(id AS INTEGER)), 0) FROM shop_product")
        max_product_id = postgres_cursor.fetchone()[0]
        
        postgres_cursor.execute("SELECT COALESCE(MAX(CAST(id AS INTEGER)), 0) FROM shop_order")
        max_order_id = postgres_cursor.fetchone()[0]
        
        print(f"📊 Current PostgreSQL max IDs - Categories: {max_category_id}, Products: {max_product_id}, Orders: {max_order_id}")
        
        # Migrate Categories
        print("\n📁 Migrating Categories...")
        sqlite_cursor.execute("SELECT * FROM shop_category")
        categories = sqlite_cursor.fetchall()
        
        # Get existing category names to avoid duplicates
        postgres_cursor.execute("SELECT name FROM shop_category")
        existing_categories = {row[0] for row in postgres_cursor.fetchall()}
        
        category_id_mapping = {}
        for category in categories:
            old_id, name, description, image = category
            
            if name not in existing_categories:
                new_id = max_category_id + 1
                max_category_id = new_id
                
                postgres_cursor.execute(
                    "INSERT INTO shop_category (id, name, description, image) VALUES (%s, %s, %s, %s)",
                    (new_id, name, description, image)
                )
                category_id_mapping[old_id] = new_id
                print(f"  ✅ Added category: {name} (ID: {old_id} -> {new_id})")
            else:
                # Find the existing category ID
                postgres_cursor.execute("SELECT id FROM shop_category WHERE name = %s", (name,))
                existing_id = postgres_cursor.fetchone()[0]
                category_id_mapping[old_id] = existing_id
                print(f"  ⏭️  Category already exists: {name} (ID: {old_id} -> {existing_id})")
        
        # Migrate Products
        print("\n🛍️  Migrating Products...")
        sqlite_cursor.execute("SELECT * FROM shop_product")
        products = sqlite_cursor.fetchall()
        
        # Get existing product names to avoid duplicates
        postgres_cursor.execute("SELECT name FROM shop_product")
        existing_products = {row[0] for row in postgres_cursor.fetchall()}
        
        product_id_mapping = {}
        for product in products:
            old_id, name, description, price, image, category_id, stock_quantity, is_featured, shipping_cost, image_url = product
            
            if name not in existing_products:
                new_id = max_product_id + 1
                max_product_id = new_id
                
                # Map the category ID
                new_category_id = category_id_mapping.get(category_id, category_id)
                
                postgres_cursor.execute(
                    """INSERT INTO shop_product 
                       (id, name, description, price, image, category_id, stock_quantity, is_featured, shipping_cost, image_url) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (new_id, name, description, price, image, new_category_id, stock_quantity, is_featured, shipping_cost, image_url)
                )
                product_id_mapping[old_id] = new_id
                print(f"  ✅ Added product: {name} (ID: {old_id} -> {new_id})")
            else:
                # Find the existing product ID
                postgres_cursor.execute("SELECT id FROM shop_product WHERE name = %s", (name,))
                existing_id = postgres_cursor.fetchone()[0]
                product_id_mapping[old_id] = existing_id
                print(f"  ⏭️  Product already exists: {name} (ID: {old_id} -> {existing_id})")
        
        # Migrate Orders
        print("\n📦 Migrating Orders...")
        sqlite_cursor.execute("SELECT * FROM shop_order")
        orders = sqlite_cursor.fetchall()
        
        for order in orders:
            old_id, customer_name, customer_email, customer_phone, address, city, country, total_amount, created_at, tracking_number = order
            
            new_id = max_order_id + 1
            max_order_id = new_id
            
            postgres_cursor.execute(
                """INSERT INTO shop_order 
                   (id, customer_name, customer_email, customer_phone, address, city, country, total_amount, created_at, tracking_number) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (new_id, customer_name, customer_email, customer_phone, address, city, country, total_amount, created_at, tracking_number)
            )
            print(f"  ✅ Added order: {customer_name} - ${total_amount} (ID: {old_id} -> {new_id})")
            
            # Migrate Order Items
            sqlite_cursor.execute("SELECT * FROM shop_orderitem WHERE order_id = ?", (old_id,))
            order_items = sqlite_cursor.fetchall()
            
            for item in order_items:
                item_id, order_id, product_id, quantity, price, product_variant_id, selected_color, selected_size = item
                
                # Map the product ID
                new_product_id = product_id_mapping.get(product_id, product_id)
                
                postgres_cursor.execute(
                    """INSERT INTO shop_orderitem 
                       (order_id, product_id, quantity, price, product_variant_id, selected_color, selected_size) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (new_id, new_product_id, quantity, price, product_variant_id, selected_color, selected_size)
                )
                print(f"    ➕ Added order item: Product {product_id} -> {new_product_id}, Qty: {quantity}")
        
        # Update sequences to avoid ID conflicts
        print("\n🔧 Updating PostgreSQL sequences...")
        postgres_cursor.execute(f"SELECT setval('shop_category_id_seq', {max_category_id})")
        postgres_cursor.execute(f"SELECT setval('shop_product_id_seq', {max_product_id})")
        postgres_cursor.execute(f"SELECT setval('shop_order_id_seq', {max_order_id})")
        
        # Commit all changes
        postgres_conn.commit()
        
        print("\n✅ Migration completed successfully!")
        
        # Show final counts
        postgres_cursor.execute("SELECT COUNT(*) FROM shop_category")
        category_count = postgres_cursor.fetchone()[0]
        
        postgres_cursor.execute("SELECT COUNT(*) FROM shop_product")
        product_count = postgres_cursor.fetchone()[0]
        
        postgres_cursor.execute("SELECT COUNT(*) FROM shop_order")
        order_count = postgres_cursor.fetchone()[0]
        
        print(f"\n📊 Final PostgreSQL counts:")
        print(f"  Categories: {category_count}")
        print(f"  Products: {product_count}")
        print(f"  Orders: {order_count}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        postgres_conn.rollback()
        raise
    
    finally:
        sqlite_conn.close()
        postgres_conn.close()

if __name__ == "__main__":
    migrate_data()