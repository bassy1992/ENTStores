# Generated manually to convert cents to dollars

from django.db import migrations
from decimal import Decimal


def convert_cents_to_dollars(apps, schema_editor):
    """Convert existing cent values to dollar values"""
    Product = apps.get_model('shop', 'Product')
    Order = apps.get_model('shop', 'Order')
    OrderItem = apps.get_model('shop', 'OrderItem')
    ProductVariant = apps.get_model('shop', 'ProductVariant')
    
    # Convert Product prices (cents to dollars)
    for product in Product.objects.all():
        if product.price:
            # Convert cents to dollars (e.g., 2500 cents = 25.00 dollars)
            product.price = Decimal(str(product.price)) / Decimal('100')
            product.save(update_fields=['price'])
    
    # Convert Order amounts
    for order in Order.objects.all():
        if order.subtotal:
            order.subtotal = Decimal(str(order.subtotal)) / Decimal('100')
        if order.shipping_cost:
            order.shipping_cost = Decimal(str(order.shipping_cost)) / Decimal('100')
        if order.tax_amount:
            order.tax_amount = Decimal(str(order.tax_amount)) / Decimal('100')
        if order.total:
            order.total = Decimal(str(order.total)) / Decimal('100')
        order.save(update_fields=['subtotal', 'shipping_cost', 'tax_amount', 'total'])
    
    # Convert OrderItem prices
    for item in OrderItem.objects.all():
        if item.unit_price:
            item.unit_price = Decimal(str(item.unit_price)) / Decimal('100')
        if item.total_price:
            item.total_price = Decimal(str(item.total_price)) / Decimal('100')
        item.save(update_fields=['unit_price', 'total_price'])
    
    # Convert ProductVariant price adjustments
    for variant in ProductVariant.objects.all():
        if variant.price_adjustment:
            variant.price_adjustment = Decimal(str(variant.price_adjustment)) / Decimal('100')
            variant.save(update_fields=['price_adjustment'])


def reverse_convert_dollars_to_cents(apps, schema_editor):
    """Reverse conversion: dollars back to cents"""
    Product = apps.get_model('shop', 'Product')
    Order = apps.get_model('shop', 'Order')
    OrderItem = apps.get_model('shop', 'OrderItem')
    ProductVariant = apps.get_model('shop', 'ProductVariant')
    
    # Convert Product prices (dollars to cents)
    for product in Product.objects.all():
        if product.price:
            product.price = int(product.price * 100)
            product.save(update_fields=['price'])
    
    # Convert Order amounts
    for order in Order.objects.all():
        if order.subtotal:
            order.subtotal = int(order.subtotal * 100)
        if order.shipping_cost:
            order.shipping_cost = int(order.shipping_cost * 100)
        if order.tax_amount:
            order.tax_amount = int(order.tax_amount * 100)
        if order.total:
            order.total = int(order.total * 100)
        order.save(update_fields=['subtotal', 'shipping_cost', 'tax_amount', 'total'])
    
    # Convert OrderItem prices
    for item in OrderItem.objects.all():
        if item.unit_price:
            item.unit_price = int(item.unit_price * 100)
        if item.total_price:
            item.total_price = int(item.total_price * 100)
        item.save(update_fields=['unit_price', 'total_price'])
    
    # Convert ProductVariant price adjustments
    for variant in ProductVariant.objects.all():
        if variant.price_adjustment:
            variant.price_adjustment = int(variant.price_adjustment * 100)
            variant.save(update_fields=['price_adjustment'])


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_convert_prices_to_dollars'),
    ]

    operations = [
        migrations.RunPython(
            convert_cents_to_dollars,
            reverse_convert_dollars_to_cents,
        ),
    ]