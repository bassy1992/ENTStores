#!/usr/bin/env python3
"""
Add Essential Environment Variables to Railway
Script to add Stripe, email, and other important variables to Railway backend
"""

import subprocess
import sys
import secrets
import string


def check_railway_cli():
    """Check if Railway CLI is installed and logged in"""
    try:
        # Check if Railway CLI is installed
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Railway CLI not found!")
            print("Install it from: https://docs.railway.app/develop/cli")
            return False
        
        print(f"✅ Railway CLI found: {result.stdout.strip()}")
        
        # Check if logged in
        result = subprocess.run(['railway', 'whoami'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Not logged in to Railway!")
            print("Run: railway login")
            return False
        
        print(f"✅ Logged in as: {result.stdout.strip()}")
        return True
        
    except FileNotFoundError:
        print("❌ Railway CLI not found!")
        print("Install it from: https://docs.railway.app/develop/cli")
        return False


def generate_secret_key():
    """Generate a secure Django secret key"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for i in range(50))


def set_railway_variable(key, value, description=""):
    """Set a single Railway environment variable"""
    try:
        # Escape special characters in the value
        escaped_value = value.replace('"', '\\"').replace('$', '\\$')
        command = f'railway variables set {key}="{escaped_value}"'
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {key}: {description}")
            return True
        else:
            print(f"❌ Failed to set {key}")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error setting {key}: {e}")
        return False


def get_user_input(prompt, required=True, sensitive=False):
    """Get user input with validation"""
    while True:
        if sensitive:
            import getpass
            value = getpass.getpass(f"{prompt}: ").strip()
        else:
            value = input(f"{prompt}: ").strip()
        
        if value or not required:
            return value
        else:
            print("This field is required. Please enter a value.")


def main():
    """Main function to set up Railway variables"""
    print("🚀 Railway Environment Variables Setup")
    print("=" * 45)
    print("This script will add essential environment variables to your Railway backend.")
    print()
    
    # Check Railway CLI
    if not check_railway_cli():
        return
    
    print("\n📋 We'll set up these variable categories:")
    print("1. Core Django settings (required)")
    print("2. Stripe payment configuration")
    print("3. Email configuration (Brevo SMTP)")
    print("4. Frontend integration")
    print("5. Security settings")
    
    proceed = input("\n🚀 Continue with setup? (y/N): ").lower() == 'y'
    if not proceed:
        print("Setup cancelled.")
        return
    
    variables_to_set = {}
    
    # 1. Core Django Settings
    print("\n🔧 Core Django Settings")
    print("=" * 25)
    
    secret_key = generate_secret_key()
    print(f"Generated secure secret key: {secret_key[:20]}...")
    
    variables_to_set.update({
        'DJANGO_SECRET_KEY': secret_key,
        'DEBUG': 'False',
        'RAILWAY_ENVIRONMENT': 'production'
    })
    
    # 2. Stripe Configuration
    print("\n💳 Stripe Payment Configuration")
    print("=" * 35)
    print("Get your keys from: https://dashboard.stripe.com/apikeys")
    
    stripe_pub = get_user_input("Stripe Publishable Key (pk_live_... or pk_test_...)", required=False)
    stripe_secret = get_user_input("Stripe Secret Key (sk_live_... or sk_test_...)", required=False, sensitive=True)
    stripe_webhook = get_user_input("Stripe Webhook Secret (whsec_...)", required=False, sensitive=True)
    
    if stripe_pub:
        variables_to_set['STRIPE_PUBLISHABLE_KEY'] = stripe_pub
    if stripe_secret:
        variables_to_set['STRIPE_SECRET_KEY'] = stripe_secret
    if stripe_webhook:
        variables_to_set['STRIPE_WEBHOOK_SECRET'] = stripe_webhook
    
    # 3. Email Configuration
    print("\n📧 Email Configuration (Brevo SMTP)")
    print("=" * 40)
    print("Get your credentials from: https://app.brevo.com/settings/keys/smtp")
    
    email_user = get_user_input("Brevo Email/Username", required=False)
    email_password = get_user_input("Brevo SMTP Password", required=False, sensitive=True)
    
    if email_user and email_password:
        variables_to_set.update({
            'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
            'EMAIL_HOST_USER': email_user,
            'EMAIL_HOST_PASSWORD': email_password,
            'DEFAULT_FROM_EMAIL': 'ENTstore <awuleynovember@gmail.com>',
            'ADMIN_EMAIL': 'Enontinoclothing@gmail.com'
        })
    
    # 4. Frontend Integration
    print("\n🌐 Frontend Integration")
    print("=" * 25)
    
    frontend_url = get_user_input("Frontend URL (e.g., https://your-app.vercel.app)", required=False)
    if frontend_url:
        variables_to_set['FRONTEND_URL'] = frontend_url
    
    # 5. Additional Settings
    print("\n⚙️  Additional Settings")
    print("=" * 22)
    
    # Add some useful defaults
    variables_to_set.update({
        'USE_SQLITE': 'False',
        'CORS_ALLOW_ALL_ORIGINS': 'False'  # More secure for production
    })
    
    # Summary
    print(f"\n📋 Summary: {len(variables_to_set)} variables to set")
    print("=" * 45)
    
    for key, value in variables_to_set.items():
        # Hide sensitive values
        if any(sensitive in key.lower() for sensitive in ['secret', 'key', 'password', 'token']):
            display_value = f"{value[:10]}..." if len(value) > 10 else "***"
        else:
            display_value = value
        print(f"  {key}: {display_value}")
    
    # Confirm deployment
    deploy = input(f"\n🚀 Deploy these {len(variables_to_set)} variables to Railway? (y/N): ").lower() == 'y'
    
    if not deploy:
        print("Deployment cancelled.")
        return
    
    # Deploy variables
    print(f"\n🔄 Deploying variables to Railway...")
    success_count = 0
    
    for key, value in variables_to_set.items():
        description = get_variable_description(key)
        if set_railway_variable(key, value, description):
            success_count += 1
    
    # Results
    print(f"\n📊 Results:")
    print(f"✅ Successfully set: {success_count}/{len(variables_to_set)} variables")
    
    if success_count == len(variables_to_set):
        print("\n🎉 All variables deployed successfully!")
        print("\n📋 Next Steps:")
        print("1. Check Railway dashboard to verify variables")
        print("2. Redeploy your application:")
        print("   railway up")
        print("3. Check deployment logs:")
        print("   railway logs")
        print("4. Test your API endpoints")
        print("5. Test Stripe payments and email notifications")
    else:
        print(f"\n⚠️  {len(variables_to_set) - success_count} variables failed to deploy")
        print("Check the errors above and try setting them manually")
    
    # Show verification commands
    print(f"\n🔍 Verification Commands:")
    print("railway variables                    # List all variables")
    print("railway logs                        # View deployment logs")
    print("railway open                        # Open Railway dashboard")


def get_variable_description(key):
    """Get description for each variable"""
    descriptions = {
        'DJANGO_SECRET_KEY': 'Django security key',
        'DEBUG': 'Debug mode (False for production)',
        'RAILWAY_ENVIRONMENT': 'Environment indicator',
        'STRIPE_PUBLISHABLE_KEY': 'Stripe public key',
        'STRIPE_SECRET_KEY': 'Stripe secret key',
        'STRIPE_WEBHOOK_SECRET': 'Stripe webhook secret',
        'EMAIL_BACKEND': 'Email backend configuration',
        'EMAIL_HOST_USER': 'SMTP username',
        'EMAIL_HOST_PASSWORD': 'SMTP password',
        'DEFAULT_FROM_EMAIL': 'Default sender email',
        'ADMIN_EMAIL': 'Admin notification email',
        'FRONTEND_URL': 'Frontend domain for CORS',
        'USE_SQLITE': 'Database preference',
        'CORS_ALLOW_ALL_ORIGINS': 'CORS security setting'
    }
    return descriptions.get(key, '')


if __name__ == '__main__':
    main()