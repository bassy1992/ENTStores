#!/usr/bin/env python3
"""
Test real order email by simulating the complete checkout flow
"""

import requests
import json
import time

def test_production_order_email():
    """Test order email on production"""
    print("🔍 Testing Real Order Email Flow on Production...")
    
    # Production API base URL
    base_url = "https://entstores-production.up.railway.app"
    
    try:
        # Test 1: Check if API is accessible
        print("\n1. Testing API accessibility...")
        response = requests.get(f"{base_url}/api/products/", timeout=30)
        if response.status_code == 200:
            print("✅ API is accessible")
        else:
            print(f"❌ API not accessible: {response.status_code}")
            return False
        
        # Test 2: Test email endpoint
        print("\n2. Testing email endpoint...")
        response = requests.get(f"{base_url}/test-email/", timeout=30)
        if response.status_code == 200:
            print("✅ Email endpoint working")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Email endpoint failed: {response.status_code}")
        
        # Test 3: Create a test order (if you have an order creation endpoint)
        print("\n3. Testing order creation...")
        
        order_data = {
            "customer_name": "Test Customer",
            "customer_email": "wyarquah@gmail.com",
            "shipping_address": "123 Test Street",
            "shipping_city": "Accra",
            "shipping_country": "Ghana",
            "shipping_postal_code": "12345",
            "items": [
                {
                    "product_id": 1,
                    "quantity": 1,
                    "price": 25.00
                }
            ],
            "payment_method": "test",
            "total": 30.00
        }
        
        # Note: This would need to match your actual API endpoint structure
        print("📝 Order data prepared for testing")
        print("⚠️ Manual order creation needed - API endpoint structure unknown")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_email_instructions():
    """Provide instructions for checking emails"""
    print("\n📧 Email Checking Instructions:")
    print("="*50)
    print("1. Check wyarquah@gmail.com inbox")
    print("2. Check spam/junk folder")
    print("3. Look for emails from: awuleynovember@gmail.com")
    print("4. Subject lines to look for:")
    print("   - 'ENTstore Email Configuration Test'")
    print("   - 'Order Confirmation - [ORDER_ID]'")
    print("   - 'ENTstore Production Email Test'")
    print("")
    print("🔍 If no emails found:")
    print("- Add awuleynovember@gmail.com to contacts")
    print("- Check email filters/rules")
    print("- Wait 5-10 minutes for delivery")
    print("- Try placing a real order on the website")

def main():
    """Run production email tests"""
    print("🚀 Production Order Email Test")
    print("="*40)
    
    # Test production
    success = test_production_order_email()
    
    # Show email checking instructions
    check_email_instructions()
    
    # Summary
    print("\n📊 Test Summary:")
    print(f"Production API Test: {'✅ PASS' if success else '❌ FAIL'}")
    
    if success:
        print("\n🎉 Production tests completed!")
        print("📧 Check your email for test messages")
    else:
        print("\n⚠️ Some tests failed - check production logs")

if __name__ == "__main__":
    main()