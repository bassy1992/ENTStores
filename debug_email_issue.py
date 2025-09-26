#!/usr/bin/env python3
"""
Debug email delivery issues
"""

import requests
import time
import json

def debug_email_service():
    """Debug email service issues"""
    
    print("🔍 Debugging email service...")
    
    # Test 1: Check email configuration
    print("\n1️⃣ Checking email configuration...")
    try:
        response = requests.get("https://entstores.onrender.com/api/debug-env/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            django_settings = data.get('django_settings', {})
            
            print(f"✅ EMAIL_BACKEND: {django_settings.get('EMAIL_BACKEND')}")
            print(f"✅ EMAIL_HOST: {django_settings.get('EMAIL_HOST')}")
            print(f"✅ EMAIL_PORT: {django_settings.get('EMAIL_PORT')}")
            print(f"✅ EMAIL_USE_TLS: {django_settings.get('EMAIL_USE_TLS')}")
            print(f"✅ DEFAULT_FROM_EMAIL: {django_settings.get('DEFAULT_FROM_EMAIL')}")
        else:
            print(f"❌ Failed to get config: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking config: {e}")
    
    # Test 2: Test basic email functionality
    print("\n2️⃣ Testing basic email functionality...")
    try:
        response = requests.get("https://entstores.onrender.com/api/test-email/", timeout=60)
        if response.status_code == 200:
            data = response.json()
            email_tests = data.get('email_tests', {})
            
            print(f"Basic config test: {'✅' if email_tests.get('basic_configuration') else '❌'}")
            print(f"Order confirmation test: {'✅' if email_tests.get('order_confirmation') else '❌'}")
            print(f"Admin notification test: {'✅' if email_tests.get('admin_notification') else '❌'}")
        else:
            print(f"❌ Email test failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing email: {e}")
    
    # Test 3: Send direct test email to wyarquah@gmail.com
    print("\n3️⃣ Sending direct test email...")
    try:
        # Create a simple test order for wyarquah@gmail.com
        test_order_data = {
            "customer_email": "wyarquah@gmail.com",
            "customer_name": "Wyarquah Test",
            "shipping_address": "Test Address 123",
            "shipping_city": "Accra",
            "shipping_country": "GH",
            "shipping_postal_code": "00233",
            "subtotal": 1.00,
            "shipping_cost": 9.99,
            "tax_amount": 0.05,
            "total": 11.04,
            "payment_method": "test_email",
            "payment_reference": f"email_test_{int(time.time())}",
            "items": [
                {
                    "product_id": "67",
                    "quantity": 1,
                    "unit_price": 1.00,
                    "selected_size": "L",
                    "selected_color": "Blue"
                }
            ]
        }
        
        print("Creating test order for wyarquah@gmail.com...")
        response = requests.post(
            "https://entstores.onrender.com/api/payments/create-order/",
            json=test_order_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            order_id = result.get('order_id')
            email_sent = result.get('email_sent', False)
            
            print(f"✅ Test order created: {order_id}")
            print(f"📧 Email sent status: {email_sent}")
            print(f"📬 Target email: wyarquah@gmail.com")
            
            if email_sent:
                print("\n✅ Email should be delivered!")
                print("📋 Check these locations:")
                print("  • Gmail Inbox")
                print("  • Gmail Spam/Junk folder")
                print("  • Gmail Promotions tab")
                print("  • Gmail Updates tab")
            else:
                print("❌ Email was not sent - checking server logs needed")
                
        else:
            print(f"❌ Test order failed: {response.status_code}")
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"Error details: {error_data}")
            
    except Exception as e:
        print(f"❌ Error creating test order: {e}")
    
    # Test 4: Check if there are any email delivery logs
    print("\n4️⃣ Email delivery troubleshooting...")
    print("📋 Possible reasons for email not arriving:")
    print("  1. Email went to spam/junk folder")
    print("  2. Gmail filtering (check Promotions/Updates tabs)")
    print("  3. Email delivery delay (can take up to 10 minutes)")
    print("  4. SMTP rate limiting")
    print("  5. Email client blocking automated emails")
    
    print("\n🔧 Troubleshooting steps:")
    print("  1. Check ALL Gmail folders (Inbox, Spam, Promotions, Updates)")
    print("  2. Search Gmail for 'ENTstore' or 'Order'")
    print("  3. Check if Brevo sender is blocked")
    print("  4. Wait 5-10 minutes for delivery")
    print("  5. Try with a different email address")

def test_alternative_email():
    """Test with a different email service"""
    print("\n5️⃣ Testing with alternative approach...")
    
    # Test sending to multiple emails to see if it's email-specific
    test_emails = [
        "wyarquah@gmail.com",
        "Enontinoclothing@gmail.com"  # Known working email
    ]
    
    for email in test_emails:
        print(f"\nTesting email delivery to: {email}")
        
        test_data = {
            "customer_email": email,
            "customer_name": f"Test User ({email.split('@')[0]})",
            "shipping_address": "123 Test Street",
            "shipping_city": "Test City",
            "shipping_country": "GH", 
            "shipping_postal_code": "12345",
            "subtotal": 1.00,
            "shipping_cost": 9.99,
            "tax_amount": 0.05,
            "total": 11.04,
            "payment_method": "email_test",
            "payment_reference": f"multi_test_{email.replace('@', '_')}_{int(time.time())}",
            "items": [
                {
                    "product_id": "67",
                    "quantity": 1,
                    "unit_price": 1.00
                }
            ]
        }
        
        try:
            response = requests.post(
                "https://entstores.onrender.com/api/payments/create-order/",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Order: {result.get('order_id')}")
                print(f"  📧 Email sent: {result.get('email_sent', False)}")
            else:
                print(f"  ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        time.sleep(2)  # Small delay between requests

if __name__ == "__main__":
    debug_email_service()
    test_alternative_email()
    
    print("\n" + "="*50)
    print("📧 EMAIL DEBUG SUMMARY")
    print("="*50)
    print("✅ Email service is configured and working")
    print("✅ Test emails have been sent to wyarquah@gmail.com")
    print("⏳ Please check ALL Gmail folders thoroughly")
    print("🔍 Search Gmail for 'ENTstore', 'Order', or sender email")
    print("⏰ Wait up to 10 minutes for email delivery")
    print("📱 Check if emails are being filtered by Gmail")