#!/usr/bin/env python3
"""
Deploy email configuration fix to production
"""

import os
import sys
import django
from django.conf import settings
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.myproject.settings')
sys.path.append('backend')
django.setup()

def check_production_email_settings():
    """Check if production email settings are correct"""
    print("🔍 Checking Production Email Settings...")
    
    required_settings = {
        'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
        'EMAIL_HOST': 'smtp-relay.brevo.com',
        'EMAIL_PORT': 587,
        'EMAIL_USE_TLS': True,
        'EMAIL_HOST_USER': '81d61b003@smtp-brevo.com',
        'DEFAULT_FROM_EMAIL': 'ENTstore <awuleynovember@gmail.com>',
        'ADMIN_EMAIL': 'Enontinoclothing@gmail.com'
    }
    
    all_correct = True
    for setting, expected in required_settings.items():
        actual = getattr(settings, setting, None)
        if actual != expected:
            print(f"❌ {setting}: Expected '{expected}', Got '{actual}'")
            all_correct = False
        else:
            print(f"✅ {setting}: {actual}")
    
    # Check password is set (don't print it)
    password = getattr(settings, 'EMAIL_HOST_PASSWORD', None)
    if password:
        print(f"✅ EMAIL_HOST_PASSWORD: Set (length: {len(password)})")
    else:
        print(f"❌ EMAIL_HOST_PASSWORD: Not set")
        all_correct = False
    
    return all_correct

def test_production_email():
    """Test email sending in production environment"""
    print("\n🔍 Testing Production Email...")
    
    try:
        from django.core.mail import send_mail
        
        result = send_mail(
            subject='ENTstore Production Email Test',
            message='This is a test email from ENTstore production environment.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['wyarquah@gmail.com'],
            fail_silently=False,
        )
        
        print(f"✅ Production email test successful! Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Production email test failed: {e}")
        return False

def create_production_order_test():
    """Create a test order in production to verify email flow"""
    print("\n🔍 Creating Production Order Test...")
    
    try:
        from shop.models import Order
        from shop.email_service import send_order_confirmation_email
        
        # Create test order
        order = Order.objects.create(
            id="PROD_TEST_" + str(int(timezone.now().timestamp())),
            customer_name="Production Test Customer",
            customer_email="wyarquah@gmail.com",
            subtotal=25.00,
            shipping_cost=5.00,
            tax_amount=0.00,
            total=30.00,
            status="pending",
            payment_method="test",
            payment_reference="test_payment",
            shipping_address="Test Production Address",
            shipping_city="Test City",
            shipping_country="Ghana",
            shipping_postal_code="12345"
        )
        
        print(f"✅ Test order created: {order.id}")
        
        # Test order confirmation email
        order_items = [
            {
                'name': 'Production Test Product',
                'quantity': 1,
                'price': '$25.00',
                'total': '$25.00'
            }
        ]
        
        success = send_order_confirmation_email(order, order_items)
        
        if success:
            print(f"✅ Production order confirmation email sent!")
        else:
            print(f"❌ Production order confirmation email failed!")
        
        # Clean up
        order.delete()
        print(f"🧹 Cleaned up test order {order.id}")
        
        return success
        
    except Exception as e:
        print(f"❌ Production order test failed: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        return False

def check_brevo_api_status():
    """Check if Brevo API is working"""
    print("\n🔍 Checking Brevo API Status...")
    
    try:
        # Check Brevo status page
        response = requests.get("https://status.brevo.com/api/v2/status.json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', {}).get('description', 'Unknown')
            print(f"✅ Brevo Status: {status}")
            return True
        else:
            print(f"⚠️ Could not check Brevo status: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ Could not check Brevo status: {e}")
        return False

def main():
    """Run all production email checks"""
    print("🚀 Production Email Configuration Check\n")
    
    # Check settings
    settings_ok = check_production_email_settings()
    
    # Check Brevo status
    brevo_ok = check_brevo_api_status()
    
    # Test email sending
    email_ok = test_production_email()
    
    # Test order flow
    order_ok = create_production_order_test()
    
    # Summary
    print("\n" + "="*60)
    print("📊 PRODUCTION EMAIL CHECK SUMMARY")
    print("="*60)
    print(f"Email Settings: {'✅ PASS' if settings_ok else '❌ FAIL'}")
    print(f"Brevo API Status: {'✅ PASS' if brevo_ok else '⚠️ WARNING'}")
    print(f"Email Sending: {'✅ PASS' if email_ok else '❌ FAIL'}")
    print(f"Order Email Flow: {'✅ PASS' if order_ok else '❌ FAIL'}")
    
    if all([settings_ok, email_ok, order_ok]):
        print("\n🎉 All production email checks passed!")
        print("📧 Check wyarquah@gmail.com for test emails.")
        print("\n📝 If you're still not receiving order emails:")
        print("1. Check your spam/junk folder")
        print("2. Add awuleynovember@gmail.com to your contacts")
        print("3. Check email filters that might be blocking emails")
        print("4. Try placing a real test order on the website")
    else:
        print("\n⚠️ Some production email checks failed.")
        print("📝 Next steps:")
        if not settings_ok:
            print("- Fix email configuration settings")
        if not email_ok:
            print("- Check SMTP credentials and network connectivity")
        if not order_ok:
            print("- Debug order email flow in production")

if __name__ == "__main__":
    from django.utils import timezone
    main()