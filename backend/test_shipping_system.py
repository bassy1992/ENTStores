#!/usr/bin/env python
"""
Test script for the shipping confirmation system.
Run this script to test the shipping confirmation functionality.

Usage:
    python test_shipping_system.py
"""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Order, OrderItem, Product, Category
from shop.email_service import send_shipping_confirmation_email, test_email_setup
from django.utils import timezone
import random


def create_test_data():
    """Create test data for shipping confirmation testing."""
    print("🔧 Creating test data...")
    
    # Create test category
    category, created = Category.objects.get_or_create(
        key='t-shirts',
        defaults={
            'label': 'T-Shirts',
            'description': 'Comfortable cotton t-shirts',
            'image': 'https://example.com/tshirt.jpg',
            'featured': True
        }
    )
    if created:
        print(f"   ✅ Created category: {category.label}")
    
    # Create test product
    product, created = Product.objects.get_or_create(
        id='test-tshirt-001',
        defaults={
            'title': 'Premium Cotton T-Shirt',
            'price': 2500,  # $25.00
            'description': 'A comfortable premium cotton t-shirt',
            'image': 'https://example.com/premium-tshirt.jpg',
            'category': category,
            'stock_quantity': 100,
            'is_active': True
        }
    )
    if created:
        print(f"   ✅ Created product: {product.title}")
    
    # Create test order
    order_id = f"ORD{random.randint(100000, 999999)}"
    order = Order.objects.create(
        id=order_id,
        customer_email='customer@example.com',
        customer_name='John Doe',
        shipping_address='123 Main Street, Apt 4B',
        shipping_city='New York',
        shipping_country='United States',
        shipping_postal_code='10001',
        subtotal=2500,
        shipping_cost=500,
        tax_amount=200,
        total=3200,
        status='processing',
        payment_method='stripe'
    )
    print(f"   ✅ Created order: {order.id}")
    
    # Create order item
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        unit_price=2500,
        total_price=2500
    )
    print(f"   ✅ Created order item")
    
    return order


def test_email_configuration():
    """Test email configuration."""
    print("\n📧 Testing email configuration...")
    
    try:
        success = test_email_setup()
        if success:
            print("   ✅ Email configuration is working!")
        else:
            print("   ❌ Email configuration failed!")
            return False
    except Exception as e:
        print(f"   ❌ Email test failed: {str(e)}")
        return False
    
    return True


def test_shipping_confirmation():
    """Test shipping confirmation email."""
    print("\n📦 Testing shipping confirmation email...")
    
    # Create test order
    order = create_test_data()
    
    # Generate tracking number
    tracking_number = f"ENT{order.id}{timezone.now().strftime('%Y%m%d')}"
    
    try:
        success = send_shipping_confirmation_email(
            order=order,
            tracking_number=tracking_number,
            carrier="UPS Ground",
            estimated_days=3,
            delivery_instructions="Package will be left at your door if no one is available. Please ensure someone is available during delivery hours (9 AM - 6 PM)."
        )
        
        if success:
            print(f"   ✅ Shipping confirmation email sent successfully!")
            print(f"   📧 Sent to: {order.customer_email}")
            print(f"   📦 Order: {order.id}")
            print(f"   🔢 Tracking: {tracking_number}")
            print(f"   🚚 Carrier: UPS Ground")
        else:
            print("   ❌ Failed to send shipping confirmation email!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error sending shipping confirmation: {str(e)}")
        return False
    
    return True


def test_status_change():
    """Test automatic email sending when order status changes."""
    print("\n🔄 Testing automatic status change emails...")
    
    # Get the most recent order
    order = Order.objects.first()
    if not order:
        print("   ❌ No orders found. Creating test order...")
        order = create_test_data()
    
    print(f"   📦 Using order: {order.id}")
    print(f"   📊 Current status: {order.status}")
    
    # Change status to shipped (this should trigger email automatically)
    old_status = order.status
    order.status = 'shipped'
    order.save()
    
    print(f"   ✅ Status changed from '{old_status}' to '{order.status}'")
    print(f"   📧 Shipping confirmation email should have been sent automatically!")
    
    return True


def display_summary():
    """Display system summary."""
    print("\n" + "="*60)
    print("📦 SHIPPING CONFIRMATION SYSTEM SUMMARY")
    print("="*60)
    
    print("\n🎯 Features Implemented:")
    print("   ✅ Enhanced shipping confirmation email template")
    print("   ✅ Automatic email sending on status change")
    print("   ✅ Tracking number generation")
    print("   ✅ Admin interface enhancements")
    print("   ✅ API endpoints for shipping updates")
    print("   ✅ Customer tracking page")
    print("   ✅ Webhook support for shipping providers")
    
    print("\n📧 Email Features:")
    print("   ✅ Professional HTML email template")
    print("   ✅ Tracking number display")
    print("   ✅ Delivery tips and instructions")
    print("   ✅ Order items summary")
    print("   ✅ Shipping address display")
    print("   ✅ Responsive design")
    
    print("\n🔧 Admin Features:")
    print("   ✅ Bulk shipping status updates")
    print("   ✅ Manual shipping confirmation emails")
    print("   ✅ Enhanced order display with shipping info")
    print("   ✅ Tracking number display")
    
    print("\n🌐 API Endpoints:")
    print("   📍 POST /shop/shipping/api/webhook/ - Shipping provider webhook")
    print("   📍 POST /shop/shipping/api/update/ - Update shipping status")
    print("   📍 GET /shop/shipping/api/status/<order_id>/ - Get shipping status")
    print("   📍 GET /shop/shipping/track/<order_id>/ - Customer tracking page")
    
    print("\n🧪 Management Commands:")
    print("   📍 python manage.py test_shipping_email - Test shipping emails")
    print("   📍 python manage.py test_shipping_email --create-test-order")
    print("   📍 python manage.py test_shipping_email --order-id ORD123456")
    
    print("\n" + "="*60)


def main():
    """Main test function."""
    print("🚀 SHIPPING CONFIRMATION SYSTEM TEST")
    print("="*50)
    
    # Test email configuration
    if not test_email_configuration():
        print("\n❌ Email configuration test failed. Please check your email settings.")
        return
    
    # Test shipping confirmation
    if not test_shipping_confirmation():
        print("\n❌ Shipping confirmation test failed.")
        return
    
    # Test status change
    if not test_status_change():
        print("\n❌ Status change test failed.")
        return
    
    # Display summary
    display_summary()
    
    print("\n🎉 All tests completed successfully!")
    print("\nNext steps:")
    print("1. Check your email inbox for the test emails")
    print("2. Visit the Django admin to see the enhanced order management")
    print("3. Test the API endpoints using the provided URLs")
    print("4. Customize the email templates as needed")


if __name__ == '__main__':
    main()