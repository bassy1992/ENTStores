#!/usr/bin/env python
"""
Railway Superuser Command
Run this script on Railway to create a superuser using Django management commands.
"""

import subprocess
import sys
import os

def run_railway_superuser():
    """Run Django management command to create superuser on Railway"""
    
    print("🚂 Creating superuser on Railway...")
    
    # Set environment variables if not already set
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    
    # Get credentials from environment or use defaults
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@entstore.com')
    password = os.environ.get('ADMIN_PASSWORD', 'EntStore2024!')
    
    try:
        # Run Django management command
        cmd = [
            sys.executable, 'manage.py', 'create_superuser',
            '--username', username,
            '--email', email,
            '--password', password
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='backend')
        
        if result.returncode == 0:
            print("✅ Superuser created successfully!")
            print(result.stdout)
        else:
            print("❌ Error creating superuser:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    print(f"\n🎉 Admin access:")
    print(f"🌐 URL: https://your-app.up.railway.app/admin/")
    print(f"👤 Username: {username}")
    print(f"🔑 Password: {password}")
    
    return True

if __name__ == '__main__':
    success = run_railway_superuser()
    sys.exit(0 if success else 1)