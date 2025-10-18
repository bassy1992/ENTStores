#!/usr/bin/env python3
"""
Deploy URL-based images functionality to Railway
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ {description} failed: {e}")
        return False


def check_git_status():
    """Check if there are changes to commit"""
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    return len(result.stdout.strip()) > 0


def main():
    """Main deployment function"""
    print("🚀 Deploying URL-Based Images to Railway")
    print("=" * 45)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("✗ Not in a git repository. Please run from project root.")
        sys.exit(1)
    
    # Check if there are changes to commit
    if not check_git_status():
        print("ℹ️  No changes to commit. Everything is up to date.")
        return
    
    # Add all changes
    if not run_command('git add .', 'Adding all changes'):
        sys.exit(1)
    
    # Commit changes
    commit_message = "Add URL-based images functionality\n\n- Added image_url field to Category model\n- Updated serializers to use get_image_url() method\n- Added sample products with URL-based images\n- Improved image handling with fallback logic"
    
    if not run_command(f'git commit -m "{commit_message}"', 'Committing changes'):
        print("ℹ️  No new changes to commit or commit failed")
    
    # Push to Railway
    if not run_command('git push origin main', 'Pushing to Railway'):
        print("✗ Failed to push to Railway")
        sys.exit(1)
    
    print("\n🎉 Deployment Complete!")
    print("\nURL-based images functionality has been deployed to Railway:")
    print("✓ Products can now use image_url field instead of file uploads")
    print("✓ Categories support image_url field")
    print("✓ API automatically serves the correct image source")
    print("✓ Sample products with URLs have been added")
    
    print("\n📋 What's New:")
    print("- Faster image loading from CDNs")
    print("- No server storage costs for images")
    print("- Easy image management via URLs")
    print("- Automatic fallback to placeholder images")
    
    print("\n🔗 Test Your Deployment:")
    print("1. Check API: https://your-railway-app.railway.app/api/products/")
    print("2. Verify images load in your frontend")
    print("3. Test Django admin for image_url fields")
    
    print("\n📚 Next Steps:")
    print("- Add more products using image URLs")
    print("- Update existing products to use CDN URLs")
    print("- Monitor image loading performance")


if __name__ == '__main__':
    main()