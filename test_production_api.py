#!/usr/bin/env python3
"""
Test production API endpoints
"""
import requests
import json

# Test different API endpoints
endpoints = [
    'https://entstores.onrender.com/api/shop/products/',
    'https://entstores.onrender.com/api/shop/products/featured/',
    'https://entstores.onrender.com/api/shop/categories/',
]

for endpoint in endpoints:
    print(f"\nTesting: {endpoint}")
    try:
        response = requests.get(endpoint, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                print(f"Success! Found {len(data['results'])} items")
                if data['results']:
                    print(f"First item keys: {list(data['results'][0].keys())}")
            else:
                print(f"Success! Response: {data}")
        else:
            print(f"Error Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("Request timed out")
    except Exception as e:
        print(f"Error: {e}")