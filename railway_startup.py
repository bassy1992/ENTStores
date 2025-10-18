#!/usr/bin/env python3
"""
Railway startup script with automatic media URL restoration
This ensures media URLs are restored every time the app starts
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """Main startup function"""
    print("🚀 Railway Startup - Media URL Preservation")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir('backend')
    
    # Run migrations
    run_command("python manage.py migrate --noinput", "Running database migrations")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Restore media URLs
    print("🔄 Restoring media URLs...")
    try:
        result = subprocess.run(
            "python manage.py restore_media_urls --auto", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            print("✅ Media URLs restored successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print("⚠️  Media URL restore completed with warnings")
            if result.stderr:
                print(result.stderr)
    except Exception as e:
        print(f"⚠️  Media URL restore failed: {e}")
    
    print("✅ Startup completed - ready to serve!")

if __name__ == "__main__":
    main()