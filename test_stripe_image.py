#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Add the backend directory to Python path
sys.path.append('backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

print("Testing Stripe checkout with product image...")

# Test data with image
checkout_data = {
    "items": [
        {
            "title": "Test Product with Image",
            "amount": 2800,
            "quantity": 1,
            "image": "/media/products/4.jpg"
        }
    ],
    "success_url": "http://localhost:8080/stripe-success",
    "cancel_url": "http://localhost:8080/cart"
}

print("Sending checkout data:")
print(json.dumps(checkout_data, indent=2))

try:
    response = requests.post(
        'http://localhost:8000/api/payments/stripe/create-checkout-session/',
        json=checkout_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        checkout_url = result.get('url')
        print(f"\n✅ Stripe checkout session created!")
        print(f"🔗 Checkout URL: {checkout_url}")
        print(f"\nYou can visit this URL to see if the product image shows up in Stripe checkout")
    else:
        print(f"❌ Failed to create checkout session")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\nCheck your Django server console for image processing logs...")