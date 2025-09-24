#!/usr/bin/env python
"""
Script to backup and restore media files for ENTstore
"""
import os
import sys
import shutil
import zipfile
from datetime import datetime
import requests

def backup_media_files():
    """Create a backup of all media files"""
    print("📦 Creating media files backup...")
    
    # Create backup directory
    backup_dir = "media_backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create timestamped backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"media_backup_{timestamp}.zip"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Check if media directory exists
    media_dir = "backend/media"
    if not os.path.exists(media_dir):
        print(f"❌ Media directory not found: {media_dir}")
        return False
    
    # Create zip backup
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, media_dir)
                zipf.write(file_path, arcname)
                print(f"   📄 Added: {arcname}")
    
    file_size = os.path.getsize(backup_path) / (1024 * 1024)  # MB
    print(f"✅ Backup created: {backup_path} ({file_size:.1f} MB)")
    return backup_path

def restore_media_files(backup_path):
    """Restore media files from backup"""
    print(f"📥 Restoring media files from: {backup_path}")
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup file not found: {backup_path}")
        return False
    
    media_dir = "backend/media"
    
    # Create media directory if it doesn't exist
    os.makedirs(media_dir, exist_ok=True)
    
    # Extract backup
    with zipfile.ZipFile(backup_path, 'r') as zipf:
        zipf.extractall(media_dir)
        print(f"✅ Restored {len(zipf.namelist())} files to {media_dir}")
    
    return True

def download_production_media():
    """Download media files from production API"""
    print("🌐 Downloading production media files...")
    
    # Get list of media files from production
    try:
        response = requests.get("https://entstores.onrender.com/api/debug-media/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            media_files = data.get('media_files', [])
            
            print(f"📋 Found {len(media_files)} media files in production")
            
            # Create local media directory
            local_media_dir = "backend/media"
            os.makedirs(local_media_dir, exist_ok=True)
            
            downloaded = 0
            for file_info in media_files:
                file_path = file_info['file']
                file_url = f"https://entstores.onrender.com/media/{file_path}"
                local_path = os.path.join(local_media_dir, file_path)
                
                # Create subdirectories if needed
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                try:
                    file_response = requests.get(file_url, timeout=30)
                    if file_response.status_code == 200:
                        with open(local_path, 'wb') as f:
                            f.write(file_response.content)
                        print(f"   ✅ Downloaded: {file_path}")
                        downloaded += 1
                    else:
                        print(f"   ❌ Failed to download: {file_path} (Status: {file_response.status_code})")
                except Exception as e:
                    print(f"   ❌ Error downloading {file_path}: {e}")
            
            print(f"✅ Downloaded {downloaded}/{len(media_files)} files")
            return downloaded > 0
            
        else:
            print(f"❌ Failed to get media list from production (Status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to production: {e}")
        return False

def list_backups():
    """List available backups"""
    backup_dir = "media_backups"
    if not os.path.exists(backup_dir):
        print("📁 No backups directory found")
        return []
    
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.zip')]
    backups.sort(reverse=True)  # Most recent first
    
    print(f"📋 Available backups ({len(backups)}):")
    for i, backup in enumerate(backups):
        backup_path = os.path.join(backup_dir, backup)
        size = os.path.getsize(backup_path) / (1024 * 1024)  # MB
        print(f"   {i+1}. {backup} ({size:.1f} MB)")
    
    return backups

def main():
    if len(sys.argv) < 2:
        print("📦 ENTstore Media Backup Tool")
        print("=" * 40)
        print("Usage:")
        print("  python backup_media.py backup          - Create backup")
        print("  python backup_media.py restore <file>  - Restore from backup")
        print("  python backup_media.py download        - Download from production")
        print("  python backup_media.py list            - List available backups")
        return
    
    command = sys.argv[1].lower()
    
    if command == "backup":
        backup_media_files()
    
    elif command == "restore":
        if len(sys.argv) < 3:
            backups = list_backups()
            if backups:
                print("\nSpecify a backup file to restore:")
                print(f"  python backup_media.py restore media_backups/{backups[0]}")
        else:
            backup_file = sys.argv[2]
            restore_media_files(backup_file)
    
    elif command == "download":
        download_production_media()
    
    elif command == "list":
        list_backups()
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()