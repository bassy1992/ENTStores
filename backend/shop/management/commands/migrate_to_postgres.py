from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Category, Product
import json


class Command(BaseCommand):
    help = 'Migrate data from SQLite to PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write("Starting data migration to PostgreSQL...")
        
        # Create superuser
        try:
            if not User.objects.filter(username='enontino').exists():
                user = User.objects.create_superuser(
                    username='enontino',
                    email='enontinoclothing@gmail.com',
                    password='admin123456'
                )
                self.stdout.write(f"✅ Created superuser: {user.username}")
            else:
                self.stdout.write("✅ Superuser already exists")
        except Exception as e:
            self.stdout.write(f"❌ Error creating superuser: {e}")
        
        # Create categories
        categories_data = [
            {'name': 'T-Shirts', 'slug': 't-shirts'},
            {'name': 'Polos', 'slug': 'polos'},
            {'name': 'Hoodies / Crewnecks', 'slug': 'hoodies'},
            {'name': 'Sweatshirts', 'slug': 'sweatshirts'},
            {'name': 'Shorts', 'slug': 'shorts'},
            {'name': 'Headwear', 'slug': 'headwear'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f"✅ Created category: {category.name}")
        
        # Create sample products
        products_data = [
            {
                'title': 'Test T-Shirt',
                'description': 'A comfortable test t-shirt',
                'price': 2500,  # $25.00
                'category': 't-shirts',
                'is_featured': True,
                'stock_quantity': 100
            },
            {
                'title': 'Wool Beanie - Charcoal',
                'description': 'Warm wool beanie in charcoal color',
                'price': 1500,  # $15.00
                'category': 'headwear',
                'is_featured': False,
                'stock_quantity': 50
            },
            {
                'title': 'Athletic Shorts - Navy',
                'description': 'Comfortable athletic shorts in navy',
                'price': 3000,  # $30.00
                'category': 'shorts',
                'is_featured': True,
                'stock_quantity': 75
            },
            {
                'title': 'Classic Polo - White',
                'description': 'Classic white polo shirt',
                'price': 3500,  # $35.00
                'category': 'polos',
                'is_featured': False,
                'stock_quantity': 60
            },
            {
                'title': 'Hoodie - Black',
                'description': 'Comfortable black hoodie',
                'price': 4500,  # $45.00
                'category': 'hoodies',
                'is_featured': True,
                'stock_quantity': 40
            }
        ]
        
        for prod_data in products_data:
            try:
                category = Category.objects.get(slug=prod_data['category'])
                product, created = Product.objects.get_or_create(
                    title=prod_data['title'],
                    defaults={
                        'description': prod_data['description'],
                        'price': prod_data['price'],
                        'category': category,
                        'is_featured': prod_data['is_featured'],
                        'stock_quantity': prod_data['stock_quantity']
                    }
                )
                if created:
                    self.stdout.write(f"✅ Created product: {product.title}")
            except Exception as e:
                self.stdout.write(f"❌ Error creating product {prod_data['title']}: {e}")
        
        # Summary
        self.stdout.write("\n📊 Migration Summary:")
        self.stdout.write(f"Users: {User.objects.count()}")
        self.stdout.write(f"Categories: {Category.objects.count()}")
        self.stdout.write(f"Products: {Product.objects.count()}")
        self.stdout.write("\n✅ Data migration completed!")