"""
Django management command to set up basic product sizes and colors.
"""

from django.core.management.base import BaseCommand
from shop.models import ProductSize, ProductColor


class Command(BaseCommand):
    help = 'Set up basic product sizes and colors for the admin'

    def handle(self, *args, **options):
        self.stdout.write("Setting up basic product options...")
        
        # Ensure we have basic sizes
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
        
        # Ensure we have basic colors
        colors_data = [
            {'name': 'Black', 'hex_code': '#000000', 'order': 1},
            {'name': 'White', 'hex_code': '#FFFFFF', 'order': 2},
            {'name': 'Navy', 'hex_code': '#1E3A8A', 'order': 3},
            {'name': 'Gray', 'hex_code': '#6B7280', 'order': 4},
            {'name': 'Red', 'hex_code': '#DC2626', 'order': 5},
            {'name': 'Blue', 'hex_code': '#2563EB', 'order': 6},
            {'name': 'Green', 'hex_code': '#059669', 'order': 7},
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
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Setup complete!\n'
                f'- Sizes available: {ProductSize.objects.count()}\n'
                f'- Colors available: {ProductColor.objects.count()}\n\n'
                f'💡 Tips for using the admin:\n'
                f'1. Go to Products → Add Product to create a new product\n'
                f'2. Scroll down to see "Product Images" and "Product Variants" sections\n'
                f'3. Use "Product Sizes" and "Product Colors" to manage available options\n'
                f'4. Select a product and use "Create basic variants" action for quick setup'
            )
        )