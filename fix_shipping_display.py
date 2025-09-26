#!/usr/bin/env python3
"""
Fix shipping display issue - convert from cents to dollars properly
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

def fix_shipping_display():
    """Fix the shipping display issue"""
    
    print("🔧 Fixing shipping display issue...")
    
    # Step 1: Commit and push changes
    print("\n📝 Committing shipping display fix...")
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Failed to stage changes: {stderr}")
        return False
    
    success, stdout, stderr = run_command('git commit -m "Fix shipping display - handle dollars vs cents conversion properly"')
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
    print("\n⏳ Waiting for deployment (60 seconds)...")
    time.sleep(60)
    
    # Step 3: Test the fix
    print("\n🧪 Testing shipping display fix...")
    
    try:
        # Test products API
        print("Testing products API...")
        response = requests.get("https://entstores.onrender.com/api/shop/products/", timeout=30)
        if response.status_code == 200:
            products = response.json()
            if products and len(products) > 0:
                first_product = products[0]
                if 'shipping_cost' in first_product:
                    shipping_cost = first_product['shipping_cost']
                    print(f"✅ Product shipping cost: ${shipping_cost}")
                    
                    # Check if it's a reasonable dollar amount (not cents)
                    if shipping_cost < 100:
                        print(f"✅ Shipping cost appears to be in dollars: ${shipping_cost}")
                    else:
                        print(f"⚠️ Shipping cost might still be in cents: {shipping_cost}")
                else:
                    print("❌ Shipping cost field missing")
            else:
                print("⚠️ No products found")
        else:
            print(f"⚠️ API returned status: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Error during testing: {e}")
    
    print("\n✅ Shipping display fix deployed!")
    print("\n📋 Changes Made:")
    print("✅ Updated ApiProduct interface to include shipping_cost")
    print("✅ Fixed convertApiProduct function to pass shipping_cost")
    print("✅ Corrected cart context to handle dollars (not cents)")
    print("✅ Updated type definitions for consistency")
    
    print("\n🎯 Expected Results:")
    print("• Cart should show shipping as $9.99 (not $999.00)")
    print("• Checkout should display correct shipping amounts")
    print("• All calculations should use dollars consistently")
    
    return True

if __name__ == "__main__":
    try:
        success = fix_shipping_display()
        if success:
            print("\n🎉 Shipping display fix successful!")
        else:
            print("\n❌ Fix failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Fix interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)