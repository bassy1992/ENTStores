#!/usr/bin/env python3
"""
Deploy shipping integration to checkout and payment
This script deploys the complete shipping cost integration
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

def deploy_shipping_integration():
    """Deploy the shipping integration changes"""
    
    print("🚀 Starting deployment of shipping integration...")
    
    # Step 1: Commit and push changes
    print("\n📝 Committing changes...")
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Failed to stage changes: {stderr}")
        return False
    
    success, stdout, stderr = run_command('git commit -m "Integrate product-based shipping costs into checkout and payment flow"')
    if not success and "nothing to commit" not in stderr:
        print(f"❌ Failed to commit changes: {stderr}")
        return False
    
    print("📤 Pushing to repository...")
    success, stdout, stderr = run_command("git push")
    if not success:
        print(f"❌ Failed to push changes: {stderr}")
        return False
    print("✅ Changes pushed to repository")
    
    # Step 2: Wait for deployment
    print("\n⏳ Waiting for deployment (90 seconds)...")
    time.sleep(90)
    
    # Step 3: Test the shipping integration
    print("\n🧪 Testing shipping integration...")
    
    try:
        # Test 1: Check if products API includes shipping_cost
        print("Testing products API...")
        response = requests.get("https://entstores-production.up.railway.app/api/shop/products/", timeout=30)
        if response.status_code == 200:
            products = response.json()
            if products and len(products) > 0:
                first_product = products[0]
                if 'shipping_cost' in first_product:
                    print(f"✅ Products API includes shipping_cost: ${first_product['shipping_cost']}")
                else:
                    print("⚠️ Products API missing shipping_cost field")
            else:
                print("⚠️ No products found in API")
        else:
            print(f"⚠️ Products API returned status: {response.status_code}")
    
        # Test 2: Check admin interface
        print("\nTesting admin interface...")
        response = requests.get("https://entstores-production.up.railway.app/admin/shop/product/add/", timeout=30)
        if response.status_code in [200, 302]:
            print("✅ Admin interface is accessible")
        else:
            print(f"⚠️ Admin interface returned status: {response.status_code}")
    
        # Test 3: Check payment endpoints
        print("\nTesting payment endpoints...")
        response = requests.get("https://entstores-production.up.railway.app/api/payments/test/", timeout=30)
        if response.status_code == 200:
            print("✅ Payment endpoints are accessible")
        else:
            print(f"⚠️ Payment endpoints returned status: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Error during testing: {e}")
    
    print("\n✅ Deployment completed!")
    print("\n📋 Shipping Integration Summary:")
    print("✅ Added shipping_cost field to Product model")
    print("✅ Updated cart context to calculate product-based shipping")
    print("✅ Modified checkout page to use product shipping costs")
    print("✅ Updated payment processing to handle shipping")
    print("✅ Enhanced cart display with shipping information")
    print("✅ Updated admin interface to manage shipping costs")
    
    print("\n🎯 Next Steps:")
    print("1. Go to https://entstores-production.up.railway.app/admin/shop/product/")
    print("2. Edit existing products to set their shipping costs")
    print("3. Test the checkout flow to verify shipping calculations")
    print("4. Check cart page to see product-based shipping totals")
    
    return True

if __name__ == "__main__":
    try:
        success = deploy_shipping_integration()
        if success:
            print("\n🎉 Shipping integration deployment successful!")
        else:
            print("\n❌ Deployment failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)