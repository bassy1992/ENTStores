#!/usr/bin/env python3
"""
Simple test for the free checkout endpoint
"""

import requests
import json

# Test data for a country that should get free checkout
test_order = {
    'customer_email': 'test@example.com',
    'customer_name': 'Test User',
    'shipping_address': '123 Test Street',
    'shipping_city': 'Test City',
    'shipping_country': 'NG',  # Nigeria - should be free checkout
    'shipping_postal_code': '12345',
    'subtotal': 50.00,
    'shipping_cost': 29.99,
    'tax_amount': 2.50,
    'total': 82.49,
    'items': [{
        'product_id': 1,
        'quantity': 1,
        'unit_price': 50.00,
        'selected_size': 'M',
        'selected_color': 'Blue'
    }]
}

def test_free_checkout():
    print("🧪 Testing Free Checkout Endpoint")
    print("=" * 40)
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/create-free-order/',
            json=test_order,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Order ID: {result.get('order_id')}")
            print(f"Status: {result.get('status')}")
            print(f"Message: {result.get('message')}")
            print(f"Payment Method: {result.get('payment_method')}")
            print(f"Country: {result.get('shipping_country')}")
        else:
            print("❌ FAILED!")
            try:
                error = response.json()
                print(f"Error: {error}")
            except:
                print(f"Response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Make sure Django server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_free_checkout()