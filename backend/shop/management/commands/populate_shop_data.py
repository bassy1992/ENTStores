from django.core.management.base import BaseCommand
from django.db import transaction
from shop.models import Category, Product, ProductTag, ProductTagAssignment


class Command(BaseCommand):
    help = 'Populate the database with initial shop data from frontend'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate shop data...'))
        
        with transaction.atomic():
            # Create categories
            self.create_categories()
            
            # Create product tags
            self.create_product_tags()
            
            # Create products
            self.create_products()
            
        self.stdout.write(self.style.SUCCESS('Successfully populated shop data!'))

    def create_categories(self):
        """Create categories based on frontend data"""
        categories_data = [
            {
                'key': 't-shirts',
                'label': 'T-Shirts',
                'description': 'Premium cotton tees with signature designs and comfortable fits',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=600',
                'featured': True,
            },
            {
                'key': 'polos',
                'label': 'Polos',
                'description': 'Classic polo shirts for smart-casual occasions',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Ff6d93005cb0342e0ae5980da9f131c00?format=webp&width=600',
                'featured': False,
            },
            {
                'key': 'hoodies',
                'label': 'Hoodies / Crewnecks',
                'description': 'Cozy hoodies and crewnecks for everyday comfort',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F65c976a3ea2e4593b4d1a27829d0f390?format=webp&width=600',
                'featured': True,
            },
            {
                'key': 'sweatshirts',
                'label': 'Sweatshirts',
                'description': 'Warm and stylish sweatshirts for cooler days',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=600',
                'featured': False,
            },
            {
                'key': 'tracksuits',
                'label': 'Tracksuits',
                'description': 'Athletic tracksuits for sport and street style',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F690488dfe67548ada8fe07090b86601f?format=webp&width=600',
                'featured': True,
            },
            {
                'key': 'jackets',
                'label': 'Jackets',
                'description': 'Versatile jackets for all seasons and occasions',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F0c4ab9be3dd740618a71b6809f4d5f28?format=webp&width=600',
                'featured': False,
            },
            {
                'key': 'shorts',
                'label': 'Shorts',
                'description': 'Comfortable shorts for active lifestyles',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=600',
                'featured': False,
            },
            {
                'key': 'headwear',
                'label': 'Headwear',
                'description': 'Caps, beanies, and hats to complete your look',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fde3830a62f2e4e32b3e515795bd471cf?format=webp&width=600',
                'featured': True,
            },
            {
                'key': 'accessories',
                'label': 'Accessories',
                'description': 'Bags, socks, and essential accessories',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=600',
                'featured': False,
            }
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                key=cat_data['key'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.label}')
            else:
                self.stdout.write(f'Category already exists: {category.label}')

    def create_product_tags(self):
        """Create product tags"""
        tags_data = [
            {'name': 'featured', 'display_name': 'Featured', 'color': '#3B82F6'},
            {'name': 'new', 'display_name': 'New', 'color': '#10B981'},
            {'name': 'bestseller', 'display_name': 'Bestseller', 'color': '#F59E0B'},
            {'name': 'sale', 'display_name': 'Sale', 'color': '#EF4444'},
        ]
        
        for tag_data in tags_data:
            tag, created = ProductTag.objects.get_or_create(
                name=tag_data['name'],
                defaults=tag_data
            )
            if created:
                self.stdout.write(f'Created tag: {tag.display_name}')

    def create_products(self):
        """Create products based on frontend data"""
        products_data = [
            {
                'id': 'track-jacket-sky',
                'title': 'ENNC Track Jacket — Sky',
                'slug': 'ennc-track-jacket-sky',
                'price': 7500,
                'description': 'Lightweight track jacket with signature ENNC chest script and retro paneling. Comfortable fit and durable zipper.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F690488dfe67548ada8fe07090b86601f?format=webp&width=800',
                'category': 'tracksuits',
                'tags': ['featured', 'new'],
                'stock_quantity': 25,
            },
            {
                'id': 'track-jacket-olive',
                'title': 'ENNC Track Jacket — Olive',
                'slug': 'ennc-track-jacket-olive',
                'price': 7500,
                'description': 'ENNC retro-inspired track jacket in olive tones. Durable construction with branded sleeve tab.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F0c4ab9be3dd740618a71b6809f4d5f28?format=webp&width=800',
                'category': 'tracksuits',
                'tags': ['featured'],
                'stock_quantity': 30,
            },
            {
                'id': 'tee-classic-black',
                'title': 'Classic Logo Tee — Black',
                'slug': 'classic-logo-tee-black',
                'price': 2800,
                'description': 'Ultra-soft cotton tee with premium screen print. Tailored athletic fit and reinforced collar for daily wear.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=800',
                'category': 't-shirts',
                'tags': ['new'],
                'stock_quantity': 50,
            },
            {
                'id': 'tee-classic-white',
                'title': 'Classic Logo Tee — White',
                'slug': 'classic-logo-tee-white',
                'price': 2800,
                'description': 'Signature logo on breathable mid‑weight cotton. Clean look that pairs with anything.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Ff6d93005cb0342e0ae5980da9f131c00?format=webp&width=800',
                'category': 't-shirts',
                'tags': ['bestseller'],
                'stock_quantity': 45,
            },
            {
                'id': 'cap-snapback',
                'title': 'Heritage Snapback Cap',
                'slug': 'heritage-snapback-cap',
                'price': 3200,
                'description': 'Structured 6‑panel snapback with curved brim, moisture-wicking band, and raised embroidery.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fde3830a62f2e4e32b3e515795bd471cf?format=webp&width=800',
                'category': 'headwear',
                'tags': [],
                'stock_quantity': 35,
            },
            {
                'id': 'duffel-weekender',
                'title': 'City Weekender Duffel',
                'slug': 'city-weekender-duffel',
                'price': 8900,
                'description': 'Durable canvas duffel with water-repellent coating, metal hardware, and removable shoulder strap.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=800',
                'category': 'accessories',
                'tags': [],
                'stock_quantity': 20,
            },
            {
                'id': 'socks-comfort',
                'title': 'Comfort Crew Socks (2‑Pack)',
                'slug': 'comfort-crew-socks',
                'price': 1600,
                'description': 'Breathable cotton blend with arch support and cushioned sole for all‑day comfort.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Ff6d93005cb0342e0ae5980da9f131c00?format=webp&width=800',
                'category': 'accessories',
                'tags': [],
                'stock_quantity': 100,
            },
            {
                'id': 'polo-navy',
                'title': 'Classic Polo — Navy',
                'slug': 'classic-polo-navy',
                'price': 4200,
                'description': 'Premium pique cotton polo with mother-of-pearl buttons and embroidered logo.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F65c976a3ea2e4593b4d1a27829d0f390?format=webp&width=800',
                'category': 'polos',
                'tags': ['new'],
                'stock_quantity': 40,
            },
            {
                'id': 'hoodie-grey',
                'title': 'Essential Hoodie — Grey',
                'slug': 'essential-hoodie-grey',
                'price': 6500,
                'description': 'Heavyweight cotton hoodie with kangaroo pocket and adjustable drawstring hood.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F7e980c238ab54fb5893ffdd1999f2c37?format=webp&width=800',
                'category': 'hoodies',
                'tags': ['featured', 'bestseller'],
                'stock_quantity': 35,
            },
            {
                'id': 'sweatshirt-cream',
                'title': 'Crewneck Sweatshirt — Cream',
                'slug': 'crewneck-sweatshirt-cream',
                'price': 5800,
                'description': 'Soft fleece-lined sweatshirt with ribbed cuffs and hem for a comfortable fit.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=800',
                'category': 'sweatshirts',
                'tags': [],
                'stock_quantity': 30,
            },
            {
                'id': 'jacket-bomber',
                'title': 'Bomber Jacket — Black',
                'slug': 'bomber-jacket-black',
                'price': 8900,
                'description': 'Classic bomber jacket with ribbed collar, cuffs, and hem. Water-resistant outer shell.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F0c4ab9be3dd740618a71b6809f4d5f28?format=webp&width=800',
                'category': 'jackets',
                'tags': ['featured'],
                'stock_quantity': 25,
            },
            {
                'id': 'shorts-athletic',
                'title': 'Athletic Shorts — Navy',
                'slug': 'athletic-shorts-navy',
                'price': 3800,
                'description': 'Lightweight athletic shorts with moisture-wicking fabric and side pockets.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F690488dfe67548ada8fe07090b86601f?format=webp&width=800',
                'category': 'shorts',
                'tags': [],
                'stock_quantity': 40,
            },
            {
                'id': 'beanie-wool',
                'title': 'Wool Beanie — Charcoal',
                'slug': 'wool-beanie-charcoal',
                'price': 2400,
                'description': 'Soft merino wool beanie with fold-over cuff and embroidered logo patch.',
                'image': 'https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fde3830a62f2e4e32b3e515795bd471cf?format=webp&width=800',
                'category': 'headwear',
                'tags': ['new'],
                'stock_quantity': 50,
            },
        ]
        
        for product_data in products_data:
            tags = product_data.pop('tags', [])
            category_key = product_data.pop('category')
            
            # Get the category instance
            try:
                category = Category.objects.get(key=category_key)
                product_data['category'] = category
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Category "{category_key}" not found for product {product_data["title"]}')
                )
                continue
            
            product, created = Product.objects.get_or_create(
                id=product_data['id'],
                defaults=product_data
            )
            
            if created:
                self.stdout.write(f'Created product: {product.title}')
                
                # Add tags
                for tag_name in tags:
                    try:
                        tag = ProductTag.objects.get(name=tag_name)
                        ProductTagAssignment.objects.get_or_create(
                            product=product,
                            tag=tag
                        )
                    except ProductTag.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'Tag "{tag_name}" not found for product {product.title}')
                        )
            else:
                self.stdout.write(f'Product already exists: {product.title}')
        
        # Update category product counts
        for category in Category.objects.all():
            category.update_product_count()
            self.stdout.write(f'Updated product count for {category.label}: {category.product_count}')