from django.core.management.base import BaseCommand
from shop.models import Product, Category
from decimal import Decimal
import json


class Command(BaseCommand):
    help = 'Add products with image URLs to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='JSON file containing product data with image URLs',
        )
        parser.add_argument(
            '--single',
            action='store_true',
            help='Add a single product interactively',
        )

    def handle(self, *args, **options):
        if options['file']:
            self.add_products_from_file(options['file'])
        elif options['single']:
            self.add_single_product()
        else:
            self.stdout.write(
                self.style.ERROR('Please specify either --file or --single option')
            )

    def add_products_from_file(self, file_path):
        """Add products from a JSON file"""
        try:
            with open(file_path, 'r') as f:
                products_data = json.load(f)
            
            for product_data in products_data:
                self.create_product(product_data)
                
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File not found: {file_path}')
            )
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON in file: {file_path}')
            )

    def add_single_product(self):
        """Add a single product interactively"""
        self.stdout.write(self.style.SUCCESS('Adding a new product with image URL'))
        
        # Get product details
        product_id = input('Product ID: ')
        title = input('Product Title: ')
        price = input('Price (e.g., 25.99): ')
        description = input('Description: ')
        image_url = input('Image URL: ')
        category_key = input('Category (t-shirts, polos, hoodies, etc.): ')
        stock_quantity = input('Stock Quantity (default 10): ') or '10'
        is_featured = input('Is Featured? (y/n, default n): ').lower() == 'y'
        
        product_data = {
            'id': product_id,
            'title': title,
            'price': price,
            'description': description,
            'image_url': image_url,
            'category': category_key,
            'stock_quantity': int(stock_quantity),
            'is_featured': is_featured
        }
        
        self.create_product(product_data)

    def create_product(self, product_data):
        """Create a product from data dictionary"""
        try:
            # Get or create category
            category, created = Category.objects.get_or_create(
                key=product_data['category'],
                defaults={
                    'label': product_data['category'].replace('-', ' ').title(),
                    'description': f'{product_data["category"].replace("-", " ").title()} category'
                }
            )
            
            # Create product
            product, created = Product.objects.get_or_create(
                id=product_data['id'],
                defaults={
                    'title': product_data['title'],
                    'price': Decimal(str(product_data['price'])),
                    'description': product_data['description'],
                    'image_url': product_data['image_url'],
                    'category': category,
                    'stock_quantity': product_data.get('stock_quantity', 10),
                    'is_featured': product_data.get('is_featured', False),
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created product: {product.title}')
                )
            else:
                # Update existing product
                product.title = product_data['title']
                product.price = Decimal(str(product_data['price']))
                product.description = product_data['description']
                product.image_url = product_data['image_url']
                product.category = category
                product.stock_quantity = product_data.get('stock_quantity', product.stock_quantity)
                product.is_featured = product_data.get('is_featured', product.is_featured)
                product.save()
                
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Updated existing product: {product.title}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating product {product_data.get("id", "unknown")}: {e}')
            )

    def get_sample_data(self):
        """Return sample product data for reference"""
        return [
            {
                "id": "ent-tshirt-001",
                "title": "ENT Classic T-Shirt",
                "price": "25.99",
                "description": "Premium cotton t-shirt with ENT logo",
                "image_url": "https://example.com/images/tshirt-001.jpg",
                "category": "t-shirts",
                "stock_quantity": 50,
                "is_featured": True
            },
            {
                "id": "ent-hoodie-001",
                "title": "ENT Premium Hoodie",
                "price": "59.99",
                "description": "Comfortable hoodie perfect for any weather",
                "image_url": "https://example.com/images/hoodie-001.jpg",
                "category": "hoodies",
                "stock_quantity": 25,
                "is_featured": False
            }
        ]