#!/usr/bin/env python3
"""
Fix production promo codes via API calls
"""

import requests
import json

def fix_production_promo_codes():
    """Fix the production promo codes by calling the admin API or direct database update"""
    
    print("🔧 Fixing Production Promo Codes")
    print("=" * 50)
    
    # Since we can't directly access the production database, let's check what we can do
    base_url = "https://entstores-production.up.railway.app/api/shop"
    
    # First, let's see what promo codes exist
    print("\n1️⃣ Checking current production promo codes...")
    try:
        response = requests.get(f"{base_url}/promo-codes/")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {data.get('count', 0)} promo codes:")
            for promo in data.get('results', []):
                print(f"   - {promo['code']}: {promo['description']} ({promo['discount_display']})")
        else:
            print(f"   Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")
    
    print("\n💡 To fix the production promo codes, you need to:")
    print("   1. Access the Django admin at: https://entstores-production.up.railway.app/admin/")
    print("   2. Go to Shop > Promo codes")
    print("   3. Edit the ENNC10 promo code:")
    print("      - Change description from 'hghjgjhg' to '10% off your entire order'")
    print("      - Change discount value from 50.00 to 10.00")
    print("      - Change maximum discount amount from 20.00 to 50.00")
    print("   4. Or delete the corrupted codes and create new ones")
    
    print("\n🔍 Testing frontend API call simulation...")
    # Test the exact same call the frontend would make
    test_data = {
        "code": "ENNC10",
        "subtotal": 25.00  # $25 in dollars (frontend converts cents to dollars)
    }
    
    try:
        response = requests.post(
            f"{base_url}/validate-promo-code/",
            json=test_data,
            headers={
                "Content-Type": "application/json",
                "Origin": "https://www.enontinoclothingstore.com"
            }
        )
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API call successful: {json.dumps(data, indent=2)}")
        else:
            print(f"   ❌ API call failed: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")

if __name__ == "__main__":
    fix_production_promo_codes()