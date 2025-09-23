"""
Django management command to add sample product variants data.
"""

from django.core.management.base import BaseCommand
from shop.models import ProductSize, ProductColor, Product, ProductVariant


class Command(BaseCommand):
    help = 'Add sample sizes, colors, and product variants'

    def handle(self, *args, **options):
        self.stdout.write("Adding sample product variant data...")
        
        # Add sizes
        sizes_data = [
            {'name': 'XS', 'display_name': 'Extra Small', 'order': 1},
            {'name': 'S', 'display_name': 'Small', 'order': 2},
            {'name': 'M', 'display_name': 'Medium', 'order': 3},
            {'name': 'L', 'display_name': 'Large', 'order': 4},
            {'name': 'XL', 'display_name': 'Extra Large', 'order': 5},
            {'name': 'XXL', 'display_name': '2X Large', 'order': 6},
        ]
        
        for size_data in sizes_data:
            size, created = ProductSize.objects.get_or_create(
                name=size_data['name'],
                defaults={
                    'display_name': size_data['display_name'],
                    'order': size_data['order']
                }
            )
            if created:
                self.stdout.write(f"✅ Created size: {size.display_name}")
        
        # Add colors
        colors_data = [
            {'name': 'Black', 'hex_code': '#000000', 'order': 1},
            {'name': 'White', 'hex_code': '#FFFFFF', 'order': 2},
            {'name': 'Navy', 'hex_code': '#1E3A8A', 'order': 3},
            {'name': 'Gray', 'hex_code': '#6B7280', 'order': 4},
            {'name': 'Red', 'hex_code': '#DC2626', 'order': 5},
            {'name': 'Blue', 'hex_code': '#2563EB', 'order': 6},
        ]
        
        for color_data in colors_data:
            color, created = ProductColor.objects.get_or_create(
                name=color_data['name'],
                defaults={
                    'hex_code': color_data['hex_code'],
                    'order': color_data['order']
                }
            )
            if created:
                self.stdout.write(f"✅ Created color: {color.name}")
        
        # Add variants for existing products
        products = Product.objects.all()[:3]  # First 3 products
        sizes = ProductSize.objects.all()[:4]  # S, M, L, XL
        colors = ProductColor.objects.all()[:3]  # First 3 colors
        
        variant_count = 0
        for product in products:
            for size in sizes:
                for color in colors:
                    variant, created = ProductVariant.objects.get_or_create(
                        product=product,
                        size=size,
                        color=color,
                        defaults={
                            'stock_quantity': 10,
                            'price_adjustment': 0,
                            'is_available': True
                        }
                    )
                    if created:
                        variant_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added sample data:\n'
                f'- Sizes: {ProductSize.objects.count()}\n'
                f'- Colors: {ProductColor.objects.count()}\n'
                f'- Variants: {ProductVariant.objects.count()}\n'
                f'- New variants created: {variant_count}'
            )
        )