#!/usr/bin/env python3
"""
Railway Environment Variables Setup Script
Interactive script to help you set up all required environment variables for Railway
"""

import secrets
import string
import subprocess
import sys
import os


def generate_secret_key():
    """Generate a secure Django secret key"""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for i in range(50))


def check_railway_cli():
    """Check if Railway CLI is installed"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def run_railway_command(command):
    """Run a Railway CLI command"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command}")
            return True
        else:
            print(f"❌ {command}")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False


def get_user_input(prompt, default=None, required=True):
    """Get user input with optional default"""
    if default:
        full_prompt = f"{prompt} (default: {default}): "
    else:
        full_prompt = f"{prompt}: "
    
    while True:
        value = input(full_prompt).strip()
        
        if value:
            return value
        elif default:
            return default
        elif not required:
            return ""
        else:
            print("This field is required. Please enter a value.")


def setup_core_variables():
    """Set up core Django variables"""
    print("\n🔧 Core Django Settings")
    print("=" * 30)
    
    # Generate secret key
    secret_key = generate_secret_key()
    print(f"Generated secure secret key: {secret_key[:20]}...")
    
    variables = {
        'DJANGO_SECRET_KEY': secret_key,
        'DEBUG': 'False',
        'RAILWAY_ENVIRONMENT': 'production'
    }
    
    return variables


def setup_payment_variables():
    """Set up payment integration variables"""
    print("\n💳 Payment Integration")
    print("=" * 25)
    
    print("Stripe Configuration:")
    stripe_pub = get_user_input("Stripe Publishable Key (pk_live_...)", required=False)
    stripe_secret = get_user_input("Stripe Secret Key (sk_live_...)", required=False)
    stripe_webhook = get_user_input("Stripe Webhook Secret (whsec_...)", required=False)
    
    variables = {}
    if stripe_pub:
        variables['STRIPE_PUBLISHABLE_KEY'] = stripe_pub
    if stripe_secret:
        variables['STRIPE_SECRET_KEY'] = stripe_secret
    if stripe_webhook:
        variables['STRIPE_WEBHOOK_SECRET'] = stripe_webhook
    
    print("\nMTN MoMo Configuration (Optional):")
    momo_key = get_user_input("MoMo Subscription Key", required=False)
    momo_user = get_user_input("MoMo API User", required=False)
    momo_api_key = get_user_input("MoMo API Key", required=False)
    
    if momo_key:
        variables['MOMO_SUBSCRIPTION_KEY'] = momo_key
    if momo_user:
        variables['MOMO_API_USER'] = momo_user
    if momo_api_key:
        variables['MOMO_API_KEY'] = momo_api_key
    
    return variables


def setup_email_variables():
    """Set up email configuration variables"""
    print("\n📧 Email Configuration")
    print("=" * 25)
    
    print("Brevo SMTP Configuration:")
    email_user = get_user_input("Brevo Email User", required=False)
    email_password = get_user_input("Brevo SMTP Password", required=False)
    
    variables = {}
    if email_user and email_password:
        variables.update({
            'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
            'EMAIL_HOST_USER': email_user,
            'EMAIL_HOST_PASSWORD': email_password,
            'DEFAULT_FROM_EMAIL': 'ENTstore <awuleynovember@gmail.com>',
            'ADMIN_EMAIL': 'Enontinoclothing@gmail.com'
        })
    
    return variables


def setup_frontend_variables():
    """Set up frontend integration variables"""
    print("\n🌐 Frontend Integration")
    print("=" * 25)
    
    frontend_url = get_user_input("Frontend URL (e.g., https://your-app.vercel.app)", required=False)
    
    variables = {}
    if frontend_url:
        variables['FRONTEND_URL'] = frontend_url
    
    return variables


def setup_storage_variables():
    """Set up file storage variables"""
    print("\n📁 File Storage (Optional)")
    print("=" * 30)
    
    print("GitHub Storage Configuration:")
    github_token = get_user_input("GitHub Personal Access Token", required=False)
    
    print("\nCloudinary Configuration:")
    cloudinary_key = get_user_input("Cloudinary API Key", required=False)
    cloudinary_secret = get_user_input("Cloudinary API Secret", required=False)
    cloudinary_name = get_user_input("Cloudinary Cloud Name", default="entstore", required=False)
    
    variables = {}
    if github_token:
        variables.update({
            'GITHUB_TOKEN': github_token,
            'GITHUB_MEDIA_REPO': 'ENTstore-media'
        })
    
    if cloudinary_key and cloudinary_secret:
        variables.update({
            'CLOUDINARY_API_KEY': cloudinary_key,
            'CLOUDINARY_API_SECRET': cloudinary_secret,
            'CLOUDINARY_CLOUD_NAME': cloudinary_name
        })
    
    return variables


def deploy_variables(variables):
    """Deploy variables to Railway"""
    print(f"\n🚀 Deploying {len(variables)} variables to Railway...")
    
    if not check_railway_cli():
        print("❌ Railway CLI not found!")
        print("Install it from: https://docs.railway.app/develop/cli")
        return False
    
    # Set variables one by one for better error handling
    success_count = 0
    for key, value in variables.items():
        # Escape special characters in the value
        escaped_value = value.replace('"', '\\"')
        command = f'railway variables set {key}="{escaped_value}"'
        
        if run_railway_command(command):
            success_count += 1
        else:
            print(f"Failed to set {key}")
    
    print(f"\n✅ Successfully set {success_count}/{len(variables)} variables")
    return success_count == len(variables)


def create_env_file(variables):
    """Create a .env file for backup"""
    filename = '.env.railway.backup'
    
    with open(filename, 'w') as f:
        f.write("# Railway Environment Variables Backup\n")
        f.write("# Generated by setup_railway_env.py\n\n")
        
        for key, value in variables.items():
            f.write(f"{key}={value}\n")
    
    print(f"📄 Created backup file: {filename}")


def main():
    """Main setup function"""
    print("🚀 Railway Environment Variables Setup")
    print("=" * 45)
    print("This script will help you set up all required environment variables for Railway.")
    print("You can skip optional sections by pressing Enter.\n")
    
    # Collect all variables
    all_variables = {}
    
    # Core variables (required)
    all_variables.update(setup_core_variables())
    
    # Payment variables
    setup_payments = input("\n💳 Set up payment integration? (y/N): ").lower() == 'y'
    if setup_payments:
        all_variables.update(setup_payment_variables())
    
    # Email variables
    setup_email = input("\n📧 Set up email configuration? (y/N): ").lower() == 'y'
    if setup_email:
        all_variables.update(setup_email_variables())
    
    # Frontend variables
    setup_frontend = input("\n🌐 Set up frontend integration? (y/N): ").lower() == 'y'
    if setup_frontend:
        all_variables.update(setup_frontend_variables())
    
    # Storage variables
    setup_storage = input("\n📁 Set up file storage? (y/N): ").lower() == 'y'
    if setup_storage:
        all_variables.update(setup_storage_variables())
    
    # Summary
    print(f"\n📋 Summary: {len(all_variables)} variables to deploy")
    print("=" * 45)
    for key, value in all_variables.items():
        # Hide sensitive values
        if any(sensitive in key.lower() for sensitive in ['secret', 'key', 'password', 'token']):
            display_value = f"{value[:10]}..." if len(value) > 10 else "***"
        else:
            display_value = value
        print(f"  {key}: {display_value}")
    
    # Create backup file
    create_env_file(all_variables)
    
    # Deploy to Railway
    deploy = input(f"\n🚀 Deploy these {len(all_variables)} variables to Railway? (y/N): ").lower() == 'y'
    
    if deploy:
        if deploy_variables(all_variables):
            print("\n🎉 All variables deployed successfully!")
            print("\nNext steps:")
            print("1. Check Railway dashboard to verify variables")
            print("2. Redeploy your application: railway up")
            print("3. Check logs: railway logs")
        else:
            print("\n⚠️  Some variables failed to deploy. Check the errors above.")
    else:
        print(f"\n📄 Variables saved to .env.railway.backup")
        print("You can deploy them manually using:")
        print("  railway variables --file .env.railway.backup")


if __name__ == '__main__':
    main()