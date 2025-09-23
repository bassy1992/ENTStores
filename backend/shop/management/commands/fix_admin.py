"""
Management command to fix admin issues and test database connectivity
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth import get_user_model
from shop.models import Category, Product, Order, OrderItem


class Command(BaseCommand):
    help = 'Fix admin issues and test database connectivity'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Fixing admin issues...'))
        
        # Test database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS('✅ Database connection: OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database connection failed: {e}'))
            return
        
        # Check if tables exist (database-agnostic)
        tables_to_check = ['shop_category', 'shop_product', 'shop_order', 'shop_orderitem']
        
        try:
            with connection.cursor() as cursor:
                # Get database engine
                db_engine = connection.settings_dict['ENGINE']
                
                if 'postgresql' in db_engine:
                    # PostgreSQL query
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' AND table_name LIKE 'shop_%'
                    """)
                elif 'sqlite' in db_engine:
                    # SQLite query
                    cursor.execute("""
                        SELECT name 
                        FROM sqlite_master 
                        WHERE type='table' AND name LIKE 'shop_%'
                    """)
                else:
                    # Generic approach - try to query each table
                    existing_tables = []
                    for table in tables_to_check:
                        try:
                            cursor.execute(f"SELECT 1 FROM {table} LIMIT 1")
                            existing_tables.append(table)
                        except:
                            pass
                    
                if 'existing_tables' not in locals():
                    existing_tables = [row[0] for row in cursor.fetchall()]
                
                self.stdout.write(f'📋 Existing shop tables: {existing_tables}')
                
                for table in tables_to_check:
                    if table in existing_tables:
                        self.stdout.write(self.style.SUCCESS(f'✅ Table {table}: EXISTS'))
                    else:
                        self.stdout.write(self.style.WARNING(f'⚠️  Table {table}: MISSING'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️  Could not check tables: {e}'))
        
        # Test model queries
        try:
            category_count = Category.objects.count()
            product_count = Product.objects.count()
            order_count = Order.objects.count()
            
            self.stdout.write(f'📊 Data counts:')
            self.stdout.write(f'   Categories: {category_count}')
            self.stdout.write(f'   Products: {product_count}')
            self.stdout.write(f'   Orders: {order_count}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Model query failed: {e}'))
            self.stdout.write('💡 Try running: python manage.py migrate')
            return
        
        # Check admin user
        User = get_user_model()
        try:
            admin_users = User.objects.filter(is_superuser=True)
            if admin_users.exists():
                self.stdout.write(self.style.SUCCESS(f'✅ Admin users found: {admin_users.count()}'))
                for user in admin_users:
                    self.stdout.write(f'   - {user.username} ({user.email})')
            else:
                self.stdout.write(self.style.WARNING('⚠️  No admin users found'))
                self.stdout.write('💡 Create one with: python manage.py createsuperuser')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Admin user check failed: {e}'))
        
        # Test a simple order query that might be causing the 500 error
        try:
            # Try to get the first order with related data
            if Order.objects.exists():
                order = Order.objects.select_related().prefetch_related('items__product').first()
                self.stdout.write(self.style.SUCCESS(f'✅ Order query test: OK (Order {order.id})'))
                
                # Test order items
                items = order.items.all()
                self.stdout.write(f'   Order has {items.count()} items')
                
            else:
                self.stdout.write(self.style.WARNING('⚠️  No orders found to test'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Order query test failed: {e}'))
            self.stdout.write('💡 This might be causing the admin 500 error')
        
        self.stdout.write(self.style.SUCCESS('🎉 Admin diagnostics completed!'))
        self.stdout.write('')
        self.stdout.write('📋 Next steps if issues found:')
        self.stdout.write('1. Run migrations: python manage.py migrate')
        self.stdout.write('2. Create superuser: python manage.py createsuperuser')
        self.stdout.write('3. Check admin at: https://entstores.onrender.com/admin/')