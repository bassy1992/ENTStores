#!/usr/bin/env python
import os
import sys
import django
import json

# Add the backend directory to Python path
sys.path.append('backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Order, OrderItem, Product
from shop.email_service import send_order_confirmation_email

print("Testing order creation and email confirmation...")

# Create a test order
try:
    # Check if we have any products
    products = Product.objects.all()[:1]
    if not products:
        print("❌ No products found in database")
        sys.exit(1)
    
    product = products[0]
    print(f"Using product: {product.title} (${product.price/100:.2f})")
    
    # Create order
    order = Order.objects.create(
        customer_email="commey120jo@gmail.com",
        customer_name="Test Customer",
        shipping_address="123 Test Street",
        shipping_city="Test City", 
        shipping_country="US",
        shipping_postal_code="12345",
        subtotal=product.price,
        shipping_cost=500,  # $5.00
        tax_amount=25,      # $0.25
        total=product.price + 500 + 25,
        payment_method="test",
        payment_reference="test_123"
    )
    
    # Create order item
    order_item = OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        unit_price=product.price
    )
    
    print(f"✅ Order created: {order.id}")
    print(f"📧 Customer email: {order.customer_email}")
    
    # Test sending order confirmation email
    print("\nSending order confirmation email...")
    success = send_order_confirmation_email(order, [order_item])
    
    if success:
        print("✅ Order confirmation email sent successfully!")
        print("Check your email at commey120jo@gmail.com")
    else:
        print("❌ Failed to send order confirmation email")
        
except Exception as e:
    print(f"❌ Error creating order: {e}")
    import traceback
    traceback.print_exc()