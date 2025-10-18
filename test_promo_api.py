#!/usr/bin/env python3
"""
Test the promo code API endpoints
"""

import requests
import json

def test_promo_code_api():
    """Test the promo code validation API"""
    
    base_url = "https://entstores-production.up.railway.app/api/shop"
    
    print("🧪 Testing Promo Code API")
    print("=" * 50)
    
    # Test 1: List available promo codes
    print("\n1️⃣ Testing promo codes list endpoint...")
    try:
        response = requests.get(f"{base_url}/promo-codes/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test 2: Validate a promo code
    print("\n2️⃣ Testing promo code validation...")
    test_data = {
        "code": "ENNC10",
        "subtotal": 50.00
    }
    
    try:
        response = requests.post(
            f"{base_url}/validate-promo-code/",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Request: {json.dumps(test_data, indent=2)}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    # Test 3: Test with invalid code
    print("\n3️⃣ Testing invalid promo code...")
    invalid_data = {
        "code": "INVALID123",
        "subtotal": 50.00
    }
    
    try:
        response = requests.post(
            f"{base_url}/validate-promo-code/",
            json=invalid_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Request: {json.dumps(invalid_data, indent=2)}")
        if response.status_code in [200, 400]:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")

if __name__ == "__main__":
    test_promo_code_api()