#!/usr/bin/env python3
"""
Test the complete order email flow
"""

import os
import sys
import django
from django.conf import settings
from django.utils import timezone
import logging

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.myproject.settings')
sys.path.append('backend')
django.setup()

from shop.models import Order, OrderItem, Product
from shop.email_service import send_order_confirmation_email

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_order():
    """Create a test order to simulate the real flow"""
    print("🔍 Creating test order...")
    
    try:
        # Create a test order
        order = Order.objects.create(
            id="TEST123",
            customer_name="Test Customer",
            customer_email="wyarquah@gmail.com",
            subtotal=45.00,
            shipping_cost=5.00,
            tax_amount=0.00,
            total=50.00,
            status="pending",
            payment_method="stripe",
            payment_reference="pi_test_123",
            shipping_address="123 Test Street",
            shipping_city="Test City",
            shipping_country="Ghana",
            shipping_postal_code="12345"
        )
        
        print(f"✅ Test order created: {order.id}")
        return order
        
    except Exception as e:
        print(f"❌ Failed to create test order: {e}")
        return None

def test_order_confirmation_email(order):
    """Test sending order confirmation email"""
    print(f"\n🔍 Testing order confirmation email for order {order.id}...")
    
    try:
        # Create mock order items
        order_items = [
            {
                'name': 'Test Product 1',
                'quantity': 1,
                'price': '$25.00',
                'total': '$25.00'
            },
            {
                'name': 'Test Product 2', 
                'quantity': 1,
                'price': '$25.00',
                'total': '$25.00'
            }
        ]
        
        # Send the email
        success = send_order_confirmation_email(order, order_items)
        
        if success:
            print(f"✅ Order confirmation email sent successfully!")
            return True
        else:
            print(f"❌ Order confirmation email failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing order confirmation email: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False

def test_payment_view_simulation():
    """Simulate what happens in the payment view"""
    print("\n🔍 Simulating payment view order confirmation flow...")
    
    order = create_test_order()
    if not order:
        return False
    
    # Simulate the payment view logic
    try:
        order_items = []  # In real flow, this would be populated from the order
        
        # This is the exact code from payment_views.py
        if order.customer_email:
            logger.info(f"Attempting to send order confirmation email to {order.customer_email} for order {order.id}")
            success = send_order_confirmation_email(order, order_items)
            if success:
                logger.info(f"✅ Order confirmation email sent successfully to {order.customer_email} for order {order.id}")
                print(f"✅ Payment view simulation successful!")
                return True
            else:
                logger.error(f"❌ Order confirmation email failed for order {order.id}")
                print(f"❌ Payment view simulation failed!")
                return False
        else:
            logger.warning(f"No customer email provided for order {order.id}")
            print(f"❌ No customer email!")
            return False
            
    except Exception as e:
        print(f"❌ Payment view simulation error: {e}")
        return False
    finally:
        # Clean up test order
        if order:
            order.delete()
            print(f"🧹 Cleaned up test order {order.id}")

def main():
    """Run all tests"""
    print("🚀 Testing Order Email Flow\n")
    
    # Test 1: Direct email service test
    order = create_test_order()
    if order:
        email_success = test_order_confirmation_email(order)
        order.delete()
        print(f"🧹 Cleaned up test order {order.id}")
    else:
        email_success = False
    
    # Test 2: Payment view simulation
    payment_view_success = test_payment_view_simulation()
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    print(f"Direct Email Service: {'✅ PASS' if email_success else '❌ FAIL'}")
    print(f"Payment View Simulation: {'✅ PASS' if payment_view_success else '❌ FAIL'}")
    
    if email_success and payment_view_success:
        print("\n🎉 All tests passed! Order email flow is working.")
        print("📧 Check wyarquah@gmail.com for test emails.")
    else:
        print("\n⚠️ Some tests failed. Check the logs above.")
        
    print("\n📝 If emails are working in tests but not in production:")
    print("1. Check production logs for errors")
    print("2. Verify environment variables are set correctly")
    print("3. Test with a real order on the website")

if __name__ == "__main__":
    main()