#!/usr/bin/env python3
"""
Comprehensive Email Test for ENTstore
Tests all email functionality and configurations
"""

import os
import sys
import django
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.myproject.settings')
sys.path.append('backend')
django.setup()

def test_smtp_connection():
    """Test direct SMTP connection"""
    print("🔍 Testing SMTP Connection...")
    
    try:
        # Get settings
        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        user = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        
        print(f"Host: {host}")
        print(f"Port: {port}")
        print(f"User: {user}")
        print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
        
        # Test connection
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(user, password)
        server.quit()
        
        print("✅ SMTP Connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ SMTP Connection failed: {e}")
        return False

def test_django_email():
    """Test Django email sending"""
    print("\n🔍 Testing Django Email...")
    
    try:
        result = send_mail(
            subject='ENTstore Email Test',
            message='This is a test email from ENTstore.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['wyarquah@gmail.com'],
            fail_silently=False,
        )
        
        print(f"✅ Django email sent successfully! Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Django email failed: {e}")
        return False

def test_order_confirmation_email():
    """Test order confirmation email template"""
    print("\n🔍 Testing Order Confirmation Email...")
    
    try:
        # Mock order data
        order_data = {
            'id': 'TEST123',
            'customer_name': 'Test Customer',
            'customer_email': 'wyarquah@gmail.com',
            'total_amount': 50.00,
            'items': [
                {'name': 'Test Product', 'quantity': 1, 'price': 50.00}
            ],
            'shipping_address': 'Test Address, Test City',
            'order_date': '2024-01-01'
        }
        
        # Create email
        subject = f'Order Confirmation - #{order_data["id"]}'
        
        # HTML content
        html_content = f"""
        <html>
        <body>
            <h2>Thank you for your order!</h2>
            <p>Dear {order_data['customer_name']},</p>
            <p>Your order #{order_data['id']} has been confirmed.</p>
            <p><strong>Total: ${order_data['total_amount']:.2f}</strong></p>
            <p>We'll send you tracking information once your order ships.</p>
            <p>Best regards,<br>ENTstore Team</p>
        </body>
        </html>
        """
        
        # Plain text content
        text_content = f"""
        Thank you for your order!
        
        Dear {order_data['customer_name']},
        
        Your order #{order_data['id']} has been confirmed.
        Total: ${order_data['total_amount']:.2f}
        
        We'll send you tracking information once your order ships.
        
        Best regards,
        ENTstore Team
        """
        
        # Send email
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order_data['customer_email']],
            reply_to=[settings.REPLY_TO_EMAIL],
        )
        email.content_subtype = 'html'
        
        result = email.send()
        
        print(f"✅ Order confirmation email sent! Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Order confirmation email failed: {e}")
        return False

def check_email_settings():
    """Check all email-related settings"""
    print("\n🔍 Checking Email Settings...")
    
    settings_to_check = [
        'EMAIL_BACKEND',
        'EMAIL_HOST',
        'EMAIL_PORT',
        'EMAIL_USE_TLS',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'DEFAULT_FROM_EMAIL',
        'ADMIN_EMAIL',
        'REPLY_TO_EMAIL'
    ]
    
    for setting in settings_to_check:
        value = getattr(settings, setting, 'NOT SET')
        if 'PASSWORD' in setting and value != 'NOT SET':
            value = '*' * len(str(value))
        print(f"{setting}: {value}")

def main():
    """Run all email tests"""
    print("🚀 Starting Comprehensive Email Test for ENTstore\n")
    
    # Check settings
    check_email_settings()
    
    # Test SMTP connection
    smtp_ok = test_smtp_connection()
    
    # Test Django email
    django_ok = test_django_email()
    
    # Test order confirmation
    order_ok = test_order_confirmation_email()
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    print(f"SMTP Connection: {'✅ PASS' if smtp_ok else '❌ FAIL'}")
    print(f"Django Email: {'✅ PASS' if django_ok else '❌ FAIL'}")
    print(f"Order Confirmation: {'✅ PASS' if order_ok else '❌ FAIL'}")
    
    if all([smtp_ok, django_ok, order_ok]):
        print("\n🎉 All tests passed! Email system is working correctly.")
        print("📧 Check wyarquah@gmail.com for test emails.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        
    print("\n📝 Next steps:")
    print("1. Check wyarquah@gmail.com for test emails")
    print("2. Verify emails arrive from awuleynovember@gmail.com")
    print("3. Test with real orders to confirm fix")

if __name__ == "__main__":
    main()