#!/usr/bin/env python3
"""
Script to add product variant models for sizes, colors, and multiple images.
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db import models
from shop.models import Product

# Let's add the new models to the models.py file
new_models_code = '''

class ProductImage(models.Model):
    """Multiple images for a product"""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="Product this image belongs to"
    )
    image = models.ImageField(
        upload_to='products/',
        help_text="Product image file"
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alternative text for the image"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Whether this is the primary product image"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order of the image"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        
    def __str__(self):
        return f"{self.product.title} - Image {self.order}"


class ProductSize(models.Model):
    """Available sizes for products"""
    
    name = models.CharField(
        max_length=10,
        unique=True,
        help_text="Size name (e.g., S, M, L, XL)"
    )
    display_name = models.CharField(
        max_length=50,
        help_text="Display name for the size"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order"
    )
    
    class Meta:
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.display_name


class ProductColor(models.Model):
    """Available colors for products"""
    
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Color name (e.g., Red, Blue, Black)"
    )
    hex_code = models.CharField(
        max_length=7,
        help_text="Hex color code (e.g., #FF0000)"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order"
    )
    
    class Meta:
        ordering = ['order', 'name']
        
    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """Product variants with specific size and color combinations"""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants',
        help_text="Product this variant belongs to"
    )
    size = models.ForeignKey(
        ProductSize,
        on_delete=models.CASCADE,
        help_text="Size of this variant"
    )
    color = models.ForeignKey(
        ProductColor,
        on_delete=models.CASCADE,
        help_text="Color of this variant"
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        help_text="Stock quantity for this specific variant"
    )
    price_adjustment = models.IntegerField(
        default=0,
        help_text="Price adjustment in cents (can be negative)"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Whether this variant is available"
    )
    
    class Meta:
        unique_together = ['product', 'size', 'color']
        
    def __str__(self):
        return f"{self.product.title} - {self.size.name} - {self.color.name}"
    
    @property
    def final_price(self):
        """Calculate final price including adjustment"""
        return self.product.price + self.price_adjustment
    
    @property
    def is_in_stock(self):
        """Check if this variant is in stock"""
        return self.stock_quantity > 0 and self.is_available
'''

print("New models code prepared. You'll need to add this to your models.py file and create migrations.")
print("\nNext steps:")
print("1. Add the new models to backend/shop/models.py")
print("2. Run: python manage.py makemigrations")
print("3. Run: python manage.py migrate")