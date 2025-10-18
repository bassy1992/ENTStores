#!/usr/bin/env python
"""
Railway Deployment with Superuser Creation
This script handles Railway deployment and creates a superuser.
"""

import subprocess
import sys
import os
import time

def run_command(cmd, description):
    """Run a command and handle output"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error in {description}: {e}")
        return False

def deploy_to_railway():
    """Deploy to Railway and create superuser"""
    
    print("🚂 Railway Deployment with Superuser Setup")
    print("=" * 50)
    
    # Check Railway CLI
    if not run_command("railway --version", "Checking Railway CLI"):
        print("❌ Railway CLI not found. Install with: npm install -g @railway/cli")
        return False
    
    # Login check
    if not run_command("railway whoami", "Checking Railway authentication"):
        print("Please login to Railway first: railway login")
        return False
    
    # Set environment variables
    print("\n🔧 Setting environment variables...")
    
    env_vars = {
        'DEBUG': 'False',
        'ADMIN_USERNAME': 'admin',
        'ADMIN_EMAIL': 'admin@entstore.com',
        'ADMIN_PASSWORD': 'EntStore2024!',
        'DJANGO_SECRET_KEY': 'your-production-secret-key-change-this'
    }
    
    for key, value in env_vars.items():
        if not run_command(f'railway variables set {key}="{value}"', f"Setting {key}"):
            print(f"⚠️  Failed to set {key}")
    
    # Deploy
    if not run_command("railway up", "Deploying to Railway"):
        return False
    
    print("\n⏳ Waiting for deployment to complete...")
    time.sleep(10)
    
    # Run migrations
    if not run_command("railway run python backend/manage.py migrate", "Running migrations"):
        print("⚠️  Migration failed, but continuing...")
    
    # Create superuser
    if not run_command("railway run python create_railway_superuser.py", "Creating superuser"):
        print("⚠️  Superuser creation failed, trying alternative method...")
        run_command("railway run python backend/manage.py create_superuser --username admin --email admin@entstore.com --password EntStore2024!", "Creating superuser (alternative)")
    
    # Collect static files
    run_command("railway run python backend/manage.py collectstatic --noinput", "Collecting static files")
    
    print("\n🎉 Deployment Complete!")
    print("=" * 50)
    print("🌐 Your app: railway open")
    print("👤 Admin panel: https://your-app.up.railway.app/admin/")
    print("📧 Username: admin")
    print("🔑 Password: EntStore2024!")
    print("\n💡 Next steps:")
    print("1. Update your domain in Railway dashboard")
    print("2. Set your real Stripe keys")
    print("3. Configure email settings")
    print("4. Change the admin password")
    
    return True

if __name__ == '__main__':
    success = deploy_to_railway()
    sys.exit(0 if success else 1)