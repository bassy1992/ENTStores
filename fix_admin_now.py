#!/usr/bin/env python
"""
Quick fix script for admin 500 error
This will make a small change to trigger a redeploy on Render
"""
import os
import subprocess
import sys
from datetime import datetime

def main():
    print("🔧 Quick Admin Fix - Triggering Redeploy")
    print("=" * 50)
    
    # Create a timestamp file to trigger redeploy
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Create/update a deployment marker file
        with open('LAST_DEPLOY.txt', 'w') as f:
            f.write(f"Admin fix deployment: {timestamp}\n")
            f.write("Fixed OrderItem admin 500 error by updating error handling\n")
        
        print(f"✅ Created deployment marker: {timestamp}")
        
        # Add and commit the change
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Fix admin 500 error - {timestamp}'], check=True)
        
        print("✅ Committed changes to git")
        
        # Push to trigger redeploy
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Pushed to main branch - this will trigger a redeploy on Render")
        print("\n🚀 Deployment Status:")
        print("1. Render will automatically detect the push")
        print("2. It will run migrations during deployment")
        print("3. The admin should be fixed after deployment completes")
        print("\n🌐 Check your admin in 2-3 minutes at:")
        print("   https://entstores.onrender.com/admin/shop/orderitem/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        print("💡 Make sure you're in a git repository and have push access")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()