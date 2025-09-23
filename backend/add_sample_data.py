#!/usr/bin/env python3
"""
Script to add sample sizes, colors, and product variants.
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import ProductSize, ProductColor, Product, ProductVariant, ProductImage

def add_sample_sizes():
    """Add sample sizes."""
    sizes_data = [
        {'name': 'XS', 'display_name': 'Extra Small', 'order': 1},
        {'name': 'S', 'display_name': 'Small', 'order': 2},
        {'name': 'M', 'display_name': 'Medium', 'order': 3},
        {'name': 'L', 'display_name': 'Large', 'order': 4},
        {'name': 'XL', 'display_name': 'Extra Large', 'order': 5},
        {'name': 'XXL', 'display_name': '2X Large', 'order': 6},
    ]
    
    print("Adding sample sizes...")
    for size_data in sizes_data:
        size, created = ProductSize.objects.get_or_create(
            name=size_data['name'],
            defaults={
                'display_name': size_data['display_name'],
                'order': size_data['order']
            }
        )
        if created:
            print(f"✅ Created size: {size.display_name}")
        else:
            print(f"🔄 Size already exists: {size.display_name}")

def add_sample_colors():
    """Add sample colors."""
    colors_data = [
        {'name': 'Black', 'hex_code': '#000000', 'order': 1},
        {'name': 'White', 'hex_code': '#FFFFFF', 'order': 2},
        {'name': 'Navy', 'hex_code': '#1E3A8A', 'order': 3},
        {'name': 'Gray', 'hex_code': '#6B7280', 'order': 4},
        {'name': 'Red', 'hex_code': '#DC2626', 'order': 5},
        {'name': 'Blue', 'hex_code': '#2563EB', 'order': 6},
        {'name': 'Green', 'hex_code': '#059669', 'order': 7},
        {'name': 'Olive', 'hex_code': '#84CC16', 'order': 8},
    ]
    
    print("Adding sample colors...")
    for color_data in colors_data:
        color, created = ProductColor.objects.get_or_create(
            name=color_data['name'],
            defaults={
                'hex_code': color_data['hex_code'],
                'order': color_data['order']
            }
        )
        if created:
            print(f"✅ Created color: {color.name} ({color.hex_code})")
        else:
            print(f"🔄 Color already exists: {color.name}")

def add_sample_variants():
    """Add sample variants for existing products."""
    print("Adding sample variants...")
    
    # Get some products to add variants to
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
                    print(f"✅ Created variant: {product.title} - {size.name} - {color.name}")
    
    print(f"Created {variant_count} variants")

def add_sample_images():
    """Add sample images for products."""
    print("Adding sample images...")
    
    # Sample image URLs
    sample_images = [
        "https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Fa03929e1731e4efcadc34cef66af98ba?format=webp&width=800",
        "https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2Ff6d93005cb0342e0ae5980da9f131c00?format=webp&width=800",
        "https://cdn.builder.io/api/v1/image/assets%2F261a98e6df434ad1ad15c1896e5c6aa3%2F65c976a3ea2e4593b4d1a27829d0f390?format=webp&width=800",
    ]
    
    products = Product.objects.all()[:3]
    image_count = 0
    
    for i, product in enumerate(products):
        for j, image_url in enumerate(sample_images):
            # Create ProductImage with URL (we'll use the image field as URL for now)
            product_image, created = ProductImage.objects.get_or_create(
                product=product,
                order=j,
                defaults={
                    'image': image_url,  # This will need to be handled properly
                    'alt_text': f'{product.title} - Image {j+1}',
                    'is_primary': j == 0,  # First image is primary
                }
            )
            if created:
                image_count += 1
                print(f"✅ Created image for {product.title} - Image {j+1}")
    
    print(f"Created {image_count} product images")

if __name__ == '__main__':
    add_sample_sizes()
    add_sample_colors()
    add_sample_variants()
    # add_sample_images()  # Skip for now as we need proper image handling
    
    print(f"\n✅ Sample data added successfully!")
    print(f"Sizes: {ProductSize.objects.count()}")
    print(f"Colors: {ProductColor.objects.count()}")
    print(f"Variants: {ProductVariant.objects.count()}")
    print(f"Images: {ProductImage.objects.count()}")