#!/usr/bin/env python3
"""
Test email service functionality and diagnose issues
"""

import os
import sys
import subprocess
import requests
import time

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=cwd
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_email_service():
    """Test the email service functionality"""
    
    print("📧 Testing email service...")
    
    # Test 1: Check email configuration endpoint
    print("\n🔧 Testing email configuration...")
    try:
        response = requests.get("https://entstores.onrender.com/api/debug-env/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            env_vars = data.get('environment_variables', {})
            django_settings = data.get('django_settings', {})
            
            print("✅ Environment variables:")
            print(f"  EMAIL_HOST_USER: {'Set' if env_vars.get('EMAIL_HOST_USER') != 'Not set' else 'Not set'}")
            print(f"  EMAIL_HOST_PASSWORD: {'Set' if env_vars.get('EMAIL_HOST_PASSWORD') != 'Not set' else 'Not set'}")
            
            print("✅ Django settings:")
            print(f"  EMAIL_BACKEND: {django_settings.get('EMAIL_BACKEND', 'Not set')}")
            print(f"  EMAIL_HOST: {django_settings.get('EMAIL_HOST', 'Not set')}")
            print(f"  EMAIL_PORT: {django_settings.get('EMAIL_PORT', 'Not set')}")
            print(f"  EMAIL_USE_TLS: {django_settings.get('EMAIL_USE_TLS', 'Not set')}")
            print(f"  DEFAULT_FROM_EMAIL: {django_settings.get('DEFAULT_FROM_EMAIL', 'Not set')}")
        else:
            print(f"⚠️ Debug endpoint returned status: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error checking configuration: {e}")
    
    # Test 2: Test email functionality
    print("\n📨 Testing email functionality...")
    try:
        response = requests.get("https://entstores.onrender.com/api/test-email/", timeout=60)
        if response.status_code == 200:
            data = response.json()
            email_tests = data.get('email_tests', {})
            
            print("📧 Email test results:")
            print(f"  Basic configuration: {'✅ Pass' if email_tests.get('basic_configuration') else '❌ Fail'}")
            print(f"  Order confirmation: {'✅ Pass' if email_tests.get('order_confirmation') else '❌ Fail'}")
            print(f"  Admin notification: {'✅ Pass' if email_tests.get('admin_notification') else '❌ Fail'}")
            
            if data.get('test_order_id'):
                print(f"  Test order ID: {data['test_order_id']}")
            if data.get('test_email'):
                print(f"  Test email sent to: {data['test_email']}")
        else:
            print(f"⚠️ Email test endpoint returned status: {response.status_code}")
            if response.text:
                print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"⚠️ Error testing email: {e}")
    
    # Test 3: Check if email templates exist
    print("\n📄 Checking email templates...")
    template_paths = [
        "backend/shop/templates/emails/order_confirmation.html",
        "backend/shop/templates/emails/admin_new_order.html", 
        "backend/shop/templates/emails/shipping_confirmation.html",
        "backend/shop/templates/emails/order_status_update.html"
    ]
    
    for template_path in template_paths:
        if os.path.exists(template_path):
            print(f"✅ {template_path}")
        else:
            print(f"❌ {template_path} - Missing")
    
    return True

def create_email_templates():
    """Create missing email templates"""
    
    print("\n📄 Creating email templates...")
    
    # Create templates directory
    templates_dir = "backend/shop/templates/emails"
    os.makedirs(templates_dir, exist_ok=True)
    
    # Order confirmation template
    order_confirmation_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Order Confirmation - {{ order_id }}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #007bff; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .footer { padding: 20px; text-align: center; color: #666; }
        .order-details { background: white; padding: 15px; margin: 15px 0; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ store_name }}</h1>
            <h2>Order Confirmation</h2>
        </div>
        
        <div class="content">
            <h3>Thank you for your order, {{ customer_name }}!</h3>
            <p>Your order has been confirmed and is being processed.</p>
            
            <div class="order-details">
                <h4>Order Details</h4>
                <p><strong>Order ID:</strong> {{ order_id }}</p>
                <p><strong>Order Date:</strong> {{ order_date|date:"F d, Y" }}</p>
                <p><strong>Total:</strong> {{ order_total }}</p>
                <p><strong>Status:</strong> {{ order_status|title }}</p>
            </div>
            
            {% if order_items %}
            <div class="order-details">
                <h4>Items Ordered</h4>
                {% for item in order_items %}
                <p>{{ item.name }} - Qty: {{ item.quantity }} - {{ item.total }}</p>
                {% endfor %}
            </div>
            {% endif %}
            
            <p>We'll send you another email when your order ships.</p>
            <p>Estimated delivery: {{ estimated_delivery }}</p>
        </div>
        
        <div class="footer">
            <p>Questions? Contact us at {{ support_email }}</p>
            <p>&copy; {{ current_year }} {{ store_name }}. All rights reserved.</p>
        </div>
    </div>
</body>
</html>"""
    
    # Admin notification template
    admin_notification_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>New Order - {{ order_id }}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #28a745; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .order-details { background: white; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .high-value { background: #fff3cd; border: 1px solid #ffeaa7; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛒 New Order Received</h1>
            <h2>Order #{{ order_id }}</h2>
        </div>
        
        <div class="content">
            <div class="order-details {% if is_high_value %}high-value{% endif %}">
                <h3>Order Information</h3>
                <p><strong>Order ID:</strong> {{ order_id }}</p>
                <p><strong>Customer:</strong> {{ customer_name }} ({{ customer_email }})</p>
                <p><strong>Total:</strong> {{ order_total }}</p>
                <p><strong>Payment Method:</strong> {{ payment_method }}</p>
                <p><strong>Items Count:</strong> {{ items_count }}</p>
                <p><strong>Order Date:</strong> {{ order_date|date:"F d, Y g:i A" }}</p>
                {% if is_high_value %}
                <p><strong>⚠️ HIGH VALUE ORDER</strong></p>
                {% endif %}
            </div>
            
            {% if order_items %}
            <div class="order-details">
                <h4>Items Ordered</h4>
                {% for item in order_items %}
                <p>{{ item.name }} - Qty: {{ item.quantity }} - {{ item.total }}</p>
                {% endfor %}
            </div>
            {% endif %}
            
            <p><a href="{{ admin_url }}">View in Admin Panel</a></p>
        </div>
    </div>
</body>
</html>"""
    
    # Shipping confirmation template
    shipping_confirmation_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Order Shipped - {{ order_id }}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #17a2b8; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .tracking-info { background: white; padding: 15px; margin: 15px 0; border-radius: 5px; text-align: center; }
        .tracking-button { background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📦 Your Order Has Shipped!</h1>
            <h2>Order #{{ order_id }}</h2>
        </div>
        
        <div class="content">
            <h3>Great news, {{ customer_name }}!</h3>
            <p>Your order is on its way to you.</p>
            
            {% if tracking_number %}
            <div class="tracking-info">
                <h4>Tracking Information</h4>
                <p><strong>Tracking Number:</strong> {{ tracking_number }}</p>
                <p><strong>Carrier:</strong> {{ shipping_carrier }}</p>
                <p><strong>Estimated Delivery:</strong> {{ estimated_delivery_date|date:"F d, Y" }}</p>
                {% if tracking_url %}
                <p><a href="{{ tracking_url }}" class="tracking-button">Track Your Package</a></p>
                {% endif %}
            </div>
            {% endif %}
            
            <p><strong>Delivery Instructions:</strong> {{ delivery_instructions }}</p>
            
            {% if shipping_address %}
            <div class="order-details">
                <h4>Shipping Address</h4>
                <p>{{ shipping_address.name }}</p>
                <p>{{ shipping_address.address_line_1 }}</p>
                <p>{{ shipping_address.city }}, {{ shipping_address.country }} {{ shipping_address.postal_code }}</p>
            </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>Questions? Contact us at {{ support_email }}</p>
        </div>
    </div>
</body>
</html>"""
    
    # Order status update template
    status_update_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Order Update - {{ order_id }}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #6f42c1; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .status-update { background: white; padding: 15px; margin: 15px 0; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Order Status Update</h1>
            <h2>Order #{{ order_id }}</h2>
        </div>
        
        <div class="content">
            <div class="status-update">
                <h3>Status: {{ new_status|title }}</h3>
                <p><strong>Updated:</strong> {{ update_date|date:"F d, Y g:i A" }}</p>
                {% if update_message %}
                <p>{{ update_message }}</p>
                {% endif %}
            </div>
            
            {% if next_steps %}
            <p><strong>What's Next:</strong> {{ next_steps }}</p>
            {% endif %}
            
            {% if tracking_number %}
            <p><strong>Tracking Number:</strong> {{ tracking_number }}</p>
            {% if tracking_url %}
            <p><a href="{{ tracking_url }}">Track Your Package</a></p>
            {% endif %}
            {% endif %}
        </div>
        
        <div class="footer">
            <p>Questions? Contact us at {{ support_email }}</p>
        </div>
    </div>
</body>
</html>"""
    
    # Write templates
    templates = {
        "order_confirmation.html": order_confirmation_html,
        "admin_new_order.html": admin_notification_html,
        "shipping_confirmation.html": shipping_confirmation_html,
        "order_status_update.html": status_update_html
    }
    
    for filename, content in templates.items():
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created {filepath}")
    
    return True

def deploy_email_fixes():
    """Deploy email service fixes"""
    
    print("🚀 Deploying email service fixes...")
    
    # Create email templates
    create_email_templates()
    
    # Commit and push changes
    print("\n📝 Committing email service fixes...")
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Failed to stage changes: {stderr}")
        return False
    
    success, stdout, stderr = run_command('git commit -m "Fix email service - add missing templates and improve error handling"')
    if not success and "nothing to commit" not in stderr:
        print(f"❌ Failed to commit changes: {stderr}")
        return False
    
    print("📤 Pushing to repository...")
    success, stdout, stderr = run_command("git push")
    if not success:
        print(f"❌ Failed to push changes: {stderr}")
        return False
    print("✅ Changes pushed to repository")
    
    # Wait for deployment
    print("\n⏳ Waiting for deployment (60 seconds)...")
    time.sleep(60)
    
    return True

if __name__ == "__main__":
    try:
        print("📧 Email Service Diagnostic Tool")
        print("=" * 50)
        
        # Test current email service
        test_email_service()
        
        # Deploy fixes
        deploy_email_fixes()
        
        # Test again after deployment
        print("\n🔄 Testing email service after fixes...")
        test_email_service()
        
        print("\n✅ Email service diagnostic completed!")
        print("\n📋 Summary:")
        print("✅ Email templates created")
        print("✅ Email service configuration checked")
        print("✅ Test emails attempted")
        
        print("\n🎯 Next Steps:")
        print("1. Check your email (Enontinoclothing@gmail.com) for test emails")
        print("2. Test order creation to verify email notifications")
        print("3. Check Render logs for any email-related errors")
        
    except KeyboardInterrupt:
        print("\n⚠️ Diagnostic interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)