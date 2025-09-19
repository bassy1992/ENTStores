#!/usr/bin/env python
"""
Simple script to test the API endpoints
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api/shop'

def test_endpoint(endpoint, description):
    print(f"\n=== Testing {description} ===")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"Results: {len(data)} items")
                if data:
                    print(f"First item: {json.dumps(data[0], indent=2)}")
            elif isinstance(data, dict):
                if 'results' in data:
                    print(f"Results: {len(data['results'])} items")
                    if data['results']:
                        print(f"First item: {json.dumps(data['results'][0], indent=2)}")
                else:
                    print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing ENNC Shop API")
    
    # Test categories
    test_endpoint('/categories/', 'Categories')
    test_endpoint('/categories/featured/', 'Featured Categories')
    
    # Test products
    test_endpoint('/products/', 'Products')
    test_endpoint('/products/featured/', 'Featured Products')
    
    # Test stats
    test_endpoint('/stats/', 'Shop Stats')
    
    # Test search
    test_endpoint('/search/?q=jacket', 'Search for "jacket"')
    
    print("\n=== API Testing Complete ===")