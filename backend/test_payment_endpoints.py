#!/usr/bin/env python
"""
Test script to verify payment endpoints are working
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_endpoint(url, method='GET', data=None, description=''):
    print(f"\n=== Testing {description} ===")
    print(f"URL: {url}")
    
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        print(f"Status: {response.status_code}")
        
        if response.status_code < 400:
            try:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
            except:
                print(f"Response: {response.text}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🧪 Testing Payment Endpoints")
    print("=" * 50)
    
    # Test configuration
    test_endpoint(f"{BASE_URL}/api/payments/test/", description="Payment Configuration")
    
    # Test Stripe checkout
    stripe_data = {
        "items": [
            {
                "title": "Test Product",
                "amount": 2500,
                "quantity": 1,
                "image": "https://via.placeholder.com/300"
            }
        ],
        "success_url": "http://localhost:8080/order-confirmation",
        "cancel_url": "http://localhost:8080/cart"
    }
    test_endpoint(f"{BASE_URL}/api/payments/stripe/create-checkout-session/", 
                 method='POST', data=stripe_data, description="Stripe Checkout Session")
    
    # Test legacy Stripe endpoint
    test_endpoint(f"{BASE_URL}/api/stripe/create-checkout-session/", 
                 method='POST', data=stripe_data, description="Legacy Stripe Endpoint")
    
    # Test MoMo initiation
    momo_data = {
        "phone": "+233501234567",
        "amount": 5000,
        "currency": "USD"
    }
    test_endpoint(f"{BASE_URL}/api/payments/momo/initiate/", 
                 method='POST', data=momo_data, description="MoMo Payment Initiation")
    
    # Test legacy MoMo endpoint
    test_endpoint(f"{BASE_URL}/api/momo/initiate/", 
                 method='POST', data=momo_data, description="Legacy MoMo Endpoint")
    
    print("\n" + "=" * 50)
    print("✅ Payment endpoint testing complete!")
    print("If you see connection errors, make sure to run:")
    print("cd backend && python manage.py runserver 8000")

if __name__ == "__main__":
    main()