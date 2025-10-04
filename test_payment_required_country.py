#!/usr/bin/env python3
"""
Test that payment-required countries are rejected by free checkout endpoint
"""

import requests
import json

# Test data for USA (should require payment)
test_order_usa = {
    'customer_email': 'test@example.com',
    'customer_name': 'Test User',
    'shipping_address': '123 Test Street',
    'shipping_city': 'New York',
    'shipping_country': 'US',  # USA - should require payment
    'shipping_postal_code': '10001',
    'subtotal': 50.00,
    'shipping_cost': 9.99,
    'tax_amount': 2.50,
    'total': 62.49,
    'items': [{
        'product_id': 1,
        'quantity': 1,
        'unit_price': 50.00,
        'selected_size': 'M',
        'selected_color': 'Blue'
    }]
}

def test_payment_required_rejection():
    print("🧪 Testing Payment Required Country Rejection")
    print("=" * 50)
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/create-free-order/',
            json=test_order_usa,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print("✅ CORRECTLY REJECTED!")
            print(f"Error: {result.get('error')}")
            print(f"Message: {result.get('message')}")
        else:
            print("❌ SHOULD HAVE BEEN REJECTED!")
            try:
                result = response.json()
                print(f"Response: {result}")
            except:
                print(f"Response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Make sure Django server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_payment_required_rejection()