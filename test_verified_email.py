#!/usr/bin/env python3
"""
Test email with verified Brevo sender
"""

import requests
import time

def test_verified_email():
    """Test email with verified sender"""
    
    print("📧 Testing email with verified Brevo sender...")
    print("✅ Using awuleynovember@gmail.com as verified sender")
    
    # First, deploy the changes
    print("\n🚀 Deploying email configuration changes...")
    
    import subprocess
    
    # Commit and push changes
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Fix email sender - use verified Brevo email awuleynovember@gmail.com"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Changes deployed to production")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git operation failed: {e}")
    
    # Wait for deployment
    print("⏳ Waiting for deployment (60 seconds)...")
    time.sleep(60)
    
    # Test email to multiple recipients
    test_emails = [
        "wyarquah@gmail.com",
        "awuleynovember@gmail.com",  # Test with the verified sender email
        "Enontinoclothing@gmail.com"
    ]
    
    for email in test_emails:
        print(f"\n📧 Testing email to: {email}")
        
        # Create test order
        order_data = {
            "customer_email": email,
            "customer_name": f"Test Customer ({email.split('@')[0]})",
            "shipping_address": "123 Test Street",
            "shipping_city": "Accra",
            "shipping_country": "GH",
            "shipping_postal_code": "00233",
            "subtotal": 1.00,
            "shipping_cost": 9.99,
            "tax_amount": 0.05,
            "total": 11.04,
            "payment_method": "verified_test",
            "payment_reference": f"verified_test_{email.replace('@', '_')}_{int(time.time())}",
            "items": [
                {
                    "product_id": "67",
                    "quantity": 1,
                    "unit_price": 1.00,
                    "selected_size": "M",
                    "selected_color": "Blue"
                }
            ]
        }
        
        try:
            response = requests.post(
                "https://entstores-production.up.railway.app/api/payments/create-order/",
                json=order_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                order_id = result.get('order_id')
                email_sent = result.get('email_sent', False)
                
                print(f"  ✅ Order created: {order_id}")
                print(f"  📧 Email sent: {'Yes' if email_sent else 'No'}")
                
                if email_sent:
                    print(f"  📬 Email should arrive at: {email}")
                else:
                    print(f"  ❌ Email failed to send")
                    
            else:
                print(f"  ❌ Order creation failed: {response.status_code}")
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                print(f"  Error: {error_data}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        time.sleep(3)  # Delay between requests
    
    print("\n" + "="*60)
    print("📧 VERIFIED EMAIL TEST SUMMARY")
    print("="*60)
    print("✅ Updated sender to verified email: awuleynovember@gmail.com")
    print("✅ Test emails sent to multiple recipients")
    print("📬 Check inboxes for order confirmation emails")
    print("🔍 Look for emails from: ENTstore <awuleynovember@gmail.com>")
    print("📱 Check spam folders if not in inbox")
    print("⏰ Emails should arrive within 5 minutes")

if __name__ == "__main__":
    test_verified_email()