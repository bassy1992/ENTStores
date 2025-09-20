from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from shop.models import Product, Category
import requests
from io import BytesIO


class Command(BaseCommand):
    help = 'Create sample products with images for testing'

    def handle(self, *args, **options):
        # Create sample categories
        electronics, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'slug': 'electronics', 'description': 'Electronic devices and gadgets'}
        )
        
        clothing, _ = Category.objects.get_or_create(
            name='Clothing',
            defaults={'slug': 'clothing', 'description': 'Fashion and apparel'}
        )

        # Sample products data
        sample_products = [
            {
                'title': 'Wireless Headphones',
                'slug': 'wireless-headphones',
                'description': 'High-quality wireless headphones with noise cancellation.',
                'price': 99.99,
                'category': electronics,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop'
            },
            {
                'title': 'Smart Watch',
                'slug': 'smart-watch',
                'description': 'Feature-rich smartwatch with health tracking.',
                'price': 199.99,
                'category': electronics,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop'
            },
            {
                'title': 'Cotton T-Shirt',
                'slug': 'cotton-t-shirt',
                'description': 'Comfortable 100% cotton t-shirt in various colors.',
                'price': 24.99,
                'category': clothing,
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop'
            },
            {
                'title': 'Denim Jeans',
                'slug': 'denim-jeans',
                'description': 'Classic denim jeans with perfect fit.',
                'price': 79.99,
                'category': clothing,
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500&h=500&fit=crop'
            },
        ]

        for product_data in sample_products:
            # Check if product already exists
            if Product.objects.filter(slug=product_data['slug']).exists():
                self.stdout.write(f"Product {product_data['title']} already exists, skipping...")
                continue

            try:
                # Download image
                response = requests.get(product_data['image_url'])
                if response.status_code == 200:
                    # Create product
                    product = Product.objects.create(
                        title=product_data['title'],
                        slug=product_data['slug'],
                        description=product_data['description'],
                        price=product_data['price'],
                        category=product_data['category'],
                        in_stock=True
                    )
                    
                    # Save image
                    image_content = ContentFile(response.content)
                    product.image.save(
                        f"{product_data['slug']}.jpg",
                        image_content,
                        save=True
                    )
                    
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created product: {product.title}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to download image for {product_data["title"]}')
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating product {product_data["title"]}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS('Sample products creation completed!')
        )