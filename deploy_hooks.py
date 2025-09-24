#!/usr/bin/env python
"""
Deployment hooks for ENTstore - ensures media files are preserved
Run this script during deployment to handle media file backup/restore
"""
import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"⚠️  {description} failed: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def pre_deployment_backup():
    """Create backup before deployment"""
    print("📦 PRE-DEPLOYMENT: Creating media backup...")
    
    # Check if we're on Render
    if not os.getenv('RENDER'):
        print("ℹ️  Not on Render, skipping backup")
        return True
    
    # Navigate to backend directory
    os.chdir('/opt/render/project/src/backend')
    
    # Create backup
    success = run_command(
        'python manage.py backup_restore_media --backup',
        'Creating media backup'
    )
    
    if success:
        # Show backup status
        run_command(
            'python manage.py backup_restore_media',
            'Checking backup status'
        )
    
    return success

def post_deployment_restore():
    """Restore media files after deployment"""
    print("📥 POST-DEPLOYMENT: Restoring media files...")
    
    # Check if we're on Render
    if not os.getenv('RENDER'):
        print("ℹ️  Not on Render, skipping restore")
        return True
    
    # Navigate to backend directory
    os.chdir('/opt/render/project/src/backend')
    
    # Auto-restore missing files
    success = run_command(
        'python manage.py backup_restore_media --auto-restore',
        'Auto-restoring missing media files'
    )
    
    # Check final status
    run_command(
        'python manage.py check_media',
        'Checking media files status'
    )
    
    return success

def emergency_restore_from_url(backup_url):
    """Emergency restore from external backup URL"""
    print(f"🚨 EMERGENCY RESTORE from: {backup_url}")
    
    os.chdir('/opt/render/project/src/backend')
    
    success = run_command(
        f'python manage.py backup_restore_media --download-from-url "{backup_url}"',
        'Emergency restore from URL'
    )
    
    if success:
        run_command(
            'python manage.py check_media',
            'Verifying restored files'
        )
    
    return success

def setup_cron_backup():
    """Set up automatic daily backups"""
    print("⏰ Setting up automatic daily backups...")
    
    cron_job = """
# ENTstore media backup - runs daily at 2 AM
0 2 * * * cd /opt/render/project/src/backend && python manage.py backup_restore_media --backup && python manage.py backup_restore_media --cleanup
"""
    
    try:
        # Write cron job (if cron is available)
        with open('/tmp/entstore_cron', 'w') as f:
            f.write(cron_job.strip())
        
        # Try to install cron job
        result = subprocess.run('crontab /tmp/entstore_cron', shell=True, capture_output=True)
        if result.returncode == 0:
            print("✅ Daily backup cron job installed")
        else:
            print("ℹ️  Cron not available, manual backups only")
        
        # Clean up
        os.remove('/tmp/entstore_cron')
        
    except Exception as e:
        print(f"ℹ️  Cron setup skipped: {e}")

def main():
    if len(sys.argv) < 2:
        print("🛡️  ENTstore Deployment Hooks")
        print("=" * 40)
        print("Usage:")
        print("  python deploy_hooks.py pre-deploy     - Create backup before deployment")
        print("  python deploy_hooks.py post-deploy    - Restore files after deployment")
        print("  python deploy_hooks.py emergency <url> - Emergency restore from URL")
        print("  python deploy_hooks.py setup-cron     - Setup automatic backups")
        print("")
        print("💡 These hooks ensure media files survive deployments")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'pre-deploy':
        success = pre_deployment_backup()
        sys.exit(0 if success else 1)
    
    elif command == 'post-deploy':
        success = post_deployment_restore()
        sys.exit(0 if success else 1)
    
    elif command == 'emergency':
        if len(sys.argv) < 3:
            print("❌ Emergency restore requires backup URL")
            sys.exit(1)
        
        backup_url = sys.argv[2]
        success = emergency_restore_from_url(backup_url)
        sys.exit(0 if success else 1)
    
    elif command == 'setup-cron':
        setup_cron_backup()
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()