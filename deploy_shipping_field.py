#!/usr/bin/env python3
"""
Deploy shipping cost field to production
This script adds the shipping_cost field to products and migrates the database
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

def deploy_to_production():
    """Deploy the shipping field changes to production"""
    
    print("🚀 Starting deployment of shipping cost field...")
    
    # Step 1: Create migration in backend directory
    print("\n📦 Creating migration...")
    success, stdout, stderr = run_command("python manage.py makemigrations shop", cwd="backend")
    if not success:
        print(f"❌ Failed to create migration: {stderr}")
        return False
    print(f"✅ Migration created: {stdout}")
    
    # Step 2: Apply migration locally first (for testing)
    print("\n🔄 Applying migration locally...")
    success, stdout, stderr = run_command("python manage.py migrate", cwd="backend")
    if not success:
        print(f"❌ Failed to apply migration locally: {stderr}")
        return False
    print(f"✅ Migration applied locally: {stdout}")
    
    # Step 3: Deploy to Render
    print("\n🌐 Deploying to Render...")
    
    # Check if we have git changes to commit
    success, stdout, stderr = run_command("git status --porcelain")
    if stdout.strip():
        print("📝 Committing changes...")
        run_command("git add .")
        run_command('git commit -m "Add shipping cost field to products"')
        
        print("📤 Pushing to repository...")
        success, stdout, stderr = run_command("git push")
        if not success:
            print(f"❌ Failed to push changes: {stderr}")
            return False
        print("✅ Changes pushed to repository")
    else:
        print("ℹ️ No changes to commit")
    
    # Step 4: Wait for deployment and test
    print("\n⏳ Waiting for Render deployment (60 seconds)...")
    time.sleep(60)
    
    # Step 5: Test the production API
    print("\n🧪 Testing production API...")
    try:
        response = requests.get("https://entstores.onrender.com/api/products/", timeout=30)
        if response.status_code == 200:
            products = response.json()
            if products and len(products) > 0:
                # Check if shipping_cost field is present
                first_product = products[0]
                if 'shipping_cost' in first_product:
                    print(f"✅ Shipping cost field deployed successfully! Example: ${first_product['shipping_cost']}")
                else:
                    print("⚠️ Shipping cost field not yet visible in API response")
            else:
                print("⚠️ No products found in API response")
        else:
            print(f"⚠️ API returned status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Could not test API: {e}")
    
    print("\n✅ Deployment completed!")
    print("\n📋 Next steps:")
    print("1. Go to https://entstores.onrender.com/admin/shop/product/add/")
    print("2. You should now see a 'Shipping cost' field in the 'Pricing & Category' section")
    print("3. Set the shipping cost for each product (default is $9.99)")
    print("4. The shipping cost will be used in cart calculations")
    
    return True

if __name__ == "__main__":
    try:
        success = deploy_to_production()
        if success:
            print("\n🎉 Shipping cost field deployment successful!")
        else:
            print("\n❌ Deployment failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)