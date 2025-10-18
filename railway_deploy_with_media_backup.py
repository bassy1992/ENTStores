#!/usr/bin/env python3
"""
Railway Deployment with Media URL Backup
This script ensures your media URLs are preserved during Railway deployments
"""
import os
import sys
import json
import subprocess
from datetime import datetime

def backup_media_urls():
    """Backup media URLs before deployment"""
    print("🔄 Backing up media URLs before deployment...")
    
    try:
        # Run the backup script
        result = subprocess.run([
            sys.executable, 'backup_restore_media_urls.py', 'backup'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Media URLs backed up successfully")
            return True
        else:
            print(f"❌ Backup failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Backup error: {e}")
        return False

def deploy_to_railway():
    """Deploy to Railway"""
    print("🚀 Deploying to Railway...")
    
    try:
        # Check if railway CLI is available
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Railway CLI not found. Install it from: https://docs.railway.app/develop/cli")
            return False
        
        # Deploy using railway up
        result = subprocess.run(['railway', 'up'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Railway deployment successful")
            return True
        else:
            print(f"❌ Railway deployment failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        return False

def wait_for_deployment():
    """Wait for deployment to be ready"""
    import time
    import requests
    
    print("⏳ Waiting for deployment to be ready...")
    
    for i in range(30):  # Wait up to 5 minutes
        try:
            response = requests.get("https://entstores-production.up.railway.app/api/health/", timeout=10)
            if response.status_code == 200:
                print("✅ Deployment is ready!")
                return True
        except:
            pass
        
        print(f"   Attempt {i+1}/30...")
        time.sleep(10)
    
    print("⚠️  Deployment might not be ready, but continuing...")
    return False

def restore_media_urls():
    """Restore media URLs after deployment"""
    print("🔄 Restoring media URLs after deployment...")
    
    try:
        # Find the latest backup file
        import glob
        backups = glob.glob('media_urls_backup_*.json')
        if not backups:
            print("❌ No backup files found")
            return False
        
        latest_backup = max(backups, key=os.path.getctime)
        print(f"Using backup: {latest_backup}")
        
        # Run the restore script
        result = subprocess.run([
            sys.executable, 'backup_restore_media_urls.py', 'restore', '--file', latest_backup
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Media URLs restored successfully")
            return True
        else:
            print(f"❌ Restore failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Restore error: {e}")
        return False

def create_railway_nixpacks_config():
    """Create nixpacks.toml for Railway deployment"""
    config_content = '''[phases.setup]
nixPkgs = ["python39", "nodejs-18_x"]

[phases.install]
cmds = [
    "pip install -r requirements.txt",
    "python backup_restore_media_urls.py backup || true"
]

[phases.build]
cmds = [
    "python manage.py collectstatic --noinput",
    "python manage.py migrate"
]

[start]
cmd = "python manage.py runserver 0.0.0.0:$PORT"

[variables]
NIXPACKS_PYTHON_VERSION = "3.9"
'''
    
    with open('nixpacks.toml', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("✅ Created nixpacks.toml for Railway")

def create_post_deploy_hook():
    """Create a post-deploy hook script"""
    hook_content = '''#!/bin/bash
# Post-deployment hook for Railway
echo "🔄 Running post-deployment tasks..."

# Restore media URLs
python backup_restore_media_urls.py restore || echo "⚠️  Media URL restore failed"

# Run any other post-deployment tasks
python manage.py migrate --noinput || echo "⚠️  Migration failed"

echo "✅ Post-deployment tasks completed"
'''
    
    with open('post_deploy.sh', 'w', encoding='utf-8') as f:
        f.write(hook_content)
    
    # Make it executable
    os.chmod('post_deploy.sh', 0o755)
    print("✅ Created post_deploy.sh hook")

def main():
    """Main deployment function"""
    print("🚀 Railway Deployment with Media URL Preservation")
    print("=" * 60)
    
    # Step 1: Backup media URLs
    if not backup_media_urls():
        print("❌ Cannot proceed without backup")
        return False
    
    # Step 2: Create Railway configuration
    create_railway_nixpacks_config()
    create_post_deploy_hook()
    
    # Step 3: Deploy to Railway
    deploy_choice = input("\n🤔 Deploy to Railway now? (y/n): ").lower().strip()
    if deploy_choice == 'y':
        if deploy_to_railway():
            # Step 4: Wait for deployment
            wait_for_deployment()
            
            # Step 5: Restore media URLs
            restore_media_urls()
            
            print("\n🎉 Deployment completed!")
            print("🔗 Check your site: https://entstores-production.up.railway.app")
        else:
            print("❌ Deployment failed")
            return False
    else:
        print("📝 Manual deployment steps:")
        print("1. Run: railway up")
        print("2. Wait for deployment to complete")
        print("3. Run: python backup_restore_media_urls.py restore")
    
    return True

if __name__ == "__main__":
    main()