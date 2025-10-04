#!/usr/bin/env python3
"""
Test script to verify the country-based checkout flow implementation.
Tests both payment-required and free checkout flows.
"""

import requests
import json
import time

# API Configuration
API_BASE = "http://localhost:8000"  # Change to your API URL
PAYMENT_ENDPOINTS = {
    'create_order': f"{API_BASE}/api/payments/create-order/",
    'create_free_order': f"{API_BASE}/api/payments/create-free-order/",
}

# Test data
TEST_ORDERS = {
    'usa_order': {
        'customer_email': 'test.usa@example.com',
        'customer_name': 'John Smith',
        'shipping_address': '123 Main Street',
        'shipping_city': 'New York',
        'shipping_country': 'US',  # USA - requires payment
        'shipping_postal_code': '10001',
        'subtotal': 50.00,
        'shipping_cost': 9.99,
        'tax_amount': 2.50,
        'total': 62.49,
        'payment_method': 'stripe',
        'payment_reference': 'test_stripe_usa_001',
        'items': [{
            'product_id': 1,
            'quantity': 2,
            'unit_price': 25.00,
            'selected_size': 'M',
            'selected_color': 'Blue'
        }]
    },
    'ghana_order': {
        'customer_email': 'test.ghana@example.com',
        'customer_name': 'Kwame Asante',
        'shipping_address': 'East Legon, Accra',
        'shipping_city': 'Accra',
        'shipping_country': 'GH',  # Ghana - requires payment
        'shipping_postal_code': 'GA-123-4567',
        'subtotal': 75.00,
        'shipping_cost': 0.00,  # Free shipping
        'tax_amount': 3.75,
        'total': 78.75,
        'payment_method': 'momo',
        'payment_reference': 'test_momo_gh_001',
        'items': [{
            'product_id': 2,
            'quantity': 1,
            'unit_price': 75.00,
            'selected_size': 'L',
            'selected_color': 'Red'
        }]
    },
    'nigeria_order': {
        'customer_email': 'test.nigeria@example.com',
        'customer_name': 'Adebayo Johnson',
        'shipping_address': 'Victoria Island, Lagos',
        'shipping_city': 'Lagos',
        'shipping_country': 'NG',  # Nigeria - free checkout
        'shipping_postal_code': '101001',
        'subtotal': 40.00,
        'shipping_cost': 29.99,
        'tax_amount': 2.00,
        'total': 71.99,
        'items': [{
            'product_id': 3,
            'quantity': 1,
            'unit_price': 40.00,
            'selected_size': 'S',
            'selected_color': 'Green'
        }]
    },
    'brazil_order': {
        'customer_email': 'test.brazil@example.com',
        'customer_name': 'Maria Silva',
        'shipping_address': 'Copacabana, Rio de Janeiro',
        'shipping_city': 'Rio de Janeiro',
        'shipping_country': 'BR',  # Brazil - free checkout
        'shipping_postal_code': '22070-900',
        'subtotal': 60.00,
        'shipping_cost': 49.99,
        'tax_amount': 3.00,
        'total': 112.99,
        'items': [{
            'product_id': 4,
            'quantity': 2,
            'unit_price': 30.00,
            'selected_size': 'M',
            'selected_color': 'Black'
        }]
    }
}

def test_payment_required_order(order_name, order_data):
    """Test order creation for countries that require payment"""
    print(f"\n🧪 Testing {order_name} (Payment Required - {order_data['shipping_country']})...")
    
    try:
        response = requests.post(
            PAYMENT_ENDPOINTS['create_order'],
            json=order_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"   📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Order created: {result.get('order_id')}")
            print(f"   💳 Payment method: {result.get('payment_method')}")
            print(f"   📧 Email sent: {result.get('email_sent', False)}")
            print(f"   🔄 Order status: {result.get('order_status')}")
            print(f"   💰 Requires payment: {result.get('requires_payment', True)}")
        else:
            result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"   ❌ Order creation failed: {result}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_free_checkout_order(order_name, order_data):
    """Test free order creation for countries that don't require payment"""
    print(f"\n🧪 Testing {order_name} (Free Checkout - {order_data['shipping_country']})...")
    
    try:
        response = requests.post(
            PAYMENT_ENDPOINTS['create_free_order'],
            json=order_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"   📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Order created: {result.get('order_id')}")
            print(f"   🆓 Payment method: {result.get('payment_method')}")
            print(f"   📧 Email sent: {result.get('email_sent', False)}")
            print(f"   🔄 Order status: {result.get('status')}")
            print(f"   🌍 Shipping country: {result.get('shipping_country')}")
        else:
            result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"   ❌ Order creation failed: {result}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_invalid_free_checkout():
    """Test that payment-required countries can't use free checkout"""
    print(f"\n🧪 Testing Invalid Free Checkout (USA should be rejected)...")
    
    usa_order = TEST_ORDERS['usa_order'].copy()
    # Remove payment info to test free checkout
    usa_order.pop('payment_method', None)
    usa_order.pop('payment_reference', None)
    
    try:
        response = requests.post(
            PAYMENT_ENDPOINTS['create_free_order'],
            json=usa_order,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"   📊 Status Code: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print(f"   ✅ Correctly rejected: {result.get('message')}")
        else:
            result = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"   ❌ Should have been rejected: {result}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    print("🚀 Testing Country-Based Checkout Flow Implementation")
    print("=" * 60)
    
    # Test payment-required countries
    print("\n📋 TESTING PAYMENT-REQUIRED COUNTRIES")
    print("-" * 40)
    test_payment_required_order("USA Order", TEST_ORDERS['usa_order'])
    test_payment_required_order("Ghana Order", TEST_ORDERS['ghana_order'])
    
    # Test free checkout countries
    print("\n📋 TESTING FREE CHECKOUT COUNTRIES")
    print("-" * 40)
    test_free_checkout_order("Nigeria Order", TEST_ORDERS['nigeria_order'])
    test_free_checkout_order("Brazil Order", TEST_ORDERS['brazil_order'])
    
    # Test invalid scenarios
    print("\n📋 TESTING INVALID SCENARIOS")
    print("-" * 40)
    test_invalid_free_checkout()
    
    print("\n" + "=" * 60)
    print("✅ Country-based checkout flow testing completed!")
    print("\n📝 Summary:")
    print("   • USA & Ghana: Require payment (Stripe/MoMo)")
    print("   • Nigeria & Brazil: Free checkout (no payment)")
    print("   • UK & Europe: Require payment (Stripe)")
    print("   • All other countries: Free checkout")

if __name__ == "__main__":
    main()