#!/usr/bin/env python3
"""
Test email with a real order creation
"""

import requests
import time

def test_order_email():
    """Test email by creating a real order"""
    
    print("📧 Testing email with real order creation...")
    
    # Create a test order
    order_data = {
        "customer_email": "wyarquah@gmail.com",
        "customer_name": "Test Customer",
        "shipping_address": "123 Test Street",
        "shipping_city": "Test City", 
        "shipping_country": "GH",
        "shipping_postal_code": "12345",
        "subtotal": 1.00,
        "shipping_cost": 9.99,
        "tax_amount": 0.05,
        "total": 11.04,
        "payment_method": "test",
        "payment_reference": "test_" + str(int(time.time())),
        "items": [
            {
                "product_id": "67",
                "quantity": 1,
                "unit_price": 1.00,
                "selected_size": "M",
                "selected_color": "Black"
            }
        ]
    }
    
    try:
        print("Creating test order...")
        response = requests.post(
            "https://entstores-production.up.railway.app/api/payments/create-order/",
            json=order_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            order_id = result.get('order_id')
            email_sent = result.get('email_sent', False)
            
            print(f"✅ Order created successfully: {order_id}")
            print(f"📧 Email sent: {'Yes' if email_sent else 'No'}")
            
            if email_sent:
                print("✅ Email should be delivered to wyarquah@gmail.com")
                print("📬 Check your inbox and spam folder")
            else:
                print("⚠️ Email was not sent - check server logs")
                
        else:
            print(f"❌ Order creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error creating test order: {e}")

if __name__ == "__main__":
    test_order_email()