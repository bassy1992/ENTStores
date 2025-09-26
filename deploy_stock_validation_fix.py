#!/usr/bin/env python3
"""
Deploy stock validation fixes to production
"""

import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ Success")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"   ❌ Failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def deploy_stock_validation():
    """Deploy the stock validation fixes"""
    print("🚀 Deploying Stock Validation Fixes")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('backend/manage.py'):
        print("❌ Error: backend/manage.py not found. Please run from project root.")
        return False
    
    print("📋 Deployment Steps:")
    print("1. Apply database migrations")
    print("2. Restart backend server")
    print("3. Test stock validation")
    print("4. Verify frontend integration")
    
    # Step 1: Apply migrations
    success = run_command(
        "cd backend && python manage.py makemigrations",
        "Creating new migrations"
    )
    
    if success:
        success = run_command(
            "cd backend && python manage.py migrate",
            "Applying database migrations"
        )
    
    # Step 2: Collect static files (if needed)
    if success:
        run_command(
            "cd backend && python manage.py collectstatic --noinput",
            "Collecting static files"
        )
    
    # Step 3: Test the backend
    if success:
        print(f"\n🧪 Testing Backend...")
        success = run_command(
            "cd backend && python manage.py check",
            "Running Django system checks"
        )
    
    # Step 4: Show next steps
    if success:
        print(f"\n✅ DEPLOYMENT SUCCESSFUL!")
        print("=" * 30)
        print("🎯 What was fixed:")
        print("   ✅ Added stock validation to order creation")
        print("   ✅ Added stock validation API endpoint")
        print("   ✅ Added automatic stock reduction after orders")
        print("   ✅ Added frontend cart stock checking")
        print("   ✅ Added comprehensive error handling")
        
        print(f"\n🔧 Next Steps:")
        print("1. Restart your backend server:")
        print("   cd backend && python manage.py runserver")
        
        print("\n2. Test the stock validation:")
        print("   python test_stock_validation.py")
        
        print("\n3. Test in browser:")
        print("   - Try adding out-of-stock items to cart")
        print("   - Try checking out with out-of-stock items")
        print("   - Verify error messages appear")
        
        print("\n4. Deploy to production:")
        print("   - Push changes to your repository")
        print("   - Deploy to your hosting platform")
        print("   - Run migrations on production")
        
        print(f"\n📊 Current Status:")
        print("   🔴 One product set to out-of-stock for testing")
        print("   🧪 Use 'ENNC Essential Hoodie — Black' to test")
        
    else:
        print(f"\n❌ DEPLOYMENT FAILED!")
        print("Please check the errors above and fix them before proceeding.")
    
    return success

if __name__ == "__main__":
    deploy_stock_validation()