#!/usr/bin/env python
"""
Pre-deployment backup script for media files
Run this before deploying to save current media files
"""
import requests
import os
import zipfile
from datetime import datetime
import json

def backup_production_media():
    """Download and backup current production media files"""
    print("📦 Backing up production media files...")
    
    # Create backup directory
    backup_dir = "production_backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Get timestamp for backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"production_media_{timestamp}.zip"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    try:
        # Get list of media files from production
        print("🔍 Getting media file list from production...")
        response = requests.get("https://entstores.onrender.com/api/debug-media/", timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Failed to get media list (Status: {response.status_code})")
            return False
        
        data = response.json()
        media_files = data.get('media_files', [])
        
        if not media_files:
            print("ℹ️  No media files found in production")
            return True
        
        print(f"📋 Found {len(media_files)} media files")
        
        # Create zip backup
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            downloaded = 0
            failed = 0
            
            for file_info in media_files:
                file_path = file_info['file']
                file_url = f"https://entstores.onrender.com/media/{file_path}"
                
                try:
                    print(f"   📥 Downloading: {file_path}")
                    file_response = requests.get(file_url, timeout=30)
                    
                    if file_response.status_code == 200:
                        # Add file to zip
                        zipf.writestr(file_path, file_response.content)
                        downloaded += 1
                    else:
                        print(f"   ⚠️  Failed to download: {file_path} (Status: {file_response.status_code})")
                        failed += 1
                        
                except Exception as e:
                    print(f"   ❌ Error downloading {file_path}: {e}")
                    failed += 1
            
            # Add metadata
            metadata = {
                "backup_date": datetime.now().isoformat(),
                "total_files": len(media_files),
                "downloaded": downloaded,
                "failed": failed,
                "source": "https://entstores.onrender.com"
            }
            zipf.writestr("backup_metadata.json", json.dumps(metadata, indent=2))
        
        file_size = os.path.getsize(backup_path) / (1024 * 1024)  # MB
        print(f"✅ Backup created: {backup_path}")
        print(f"📊 Downloaded: {downloaded}/{len(media_files)} files ({file_size:.1f} MB)")
        
        if failed > 0:
            print(f"⚠️  {failed} files failed to download")
        
        return True
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def restore_media_backup(backup_path):
    """Restore media files from backup to local directory"""
    print(f"📥 Restoring media from: {backup_path}")
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup file not found: {backup_path}")
        return False
    
    # Create local media directory
    media_dir = "backend/media"
    os.makedirs(media_dir, exist_ok=True)
    
    try:
        with zipfile.ZipFile(backup_path, 'r') as zipf:
            # Extract all files except metadata
            files_extracted = 0
            for file_info in zipf.filelist:
                if file_info.filename != "backup_metadata.json":
                    zipf.extract(file_info, media_dir)
                    files_extracted += 1
            
            # Show metadata if available
            try:
                metadata_content = zipf.read("backup_metadata.json")
                metadata = json.loads(metadata_content)
                print(f"📊 Backup info:")
                print(f"   Date: {metadata.get('backup_date', 'Unknown')}")
                print(f"   Source: {metadata.get('source', 'Unknown')}")
                print(f"   Original files: {metadata.get('total_files', 'Unknown')}")
            except:
                pass
            
            print(f"✅ Restored {files_extracted} files to {media_dir}")
            return True
            
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False

def list_backups():
    """List available backups"""
    backup_dir = "production_backups"
    if not os.path.exists(backup_dir):
        print("📁 No backups directory found")
        return []
    
    backups = [f for f in os.listdir(backup_dir) if f.endswith('.zip')]
    backups.sort(reverse=True)  # Most recent first
    
    print(f"📋 Available production backups ({len(backups)}):")
    for i, backup in enumerate(backups):
        backup_path = os.path.join(backup_dir, backup)
        size = os.path.getsize(backup_path) / (1024 * 1024)  # MB
        print(f"   {i+1}. {backup} ({size:.1f} MB)")
    
    return backups

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("📦 Production Media Backup Tool")
        print("=" * 40)
        print("Usage:")
        print("  python pre_deploy_backup.py backup           - Backup production media")
        print("  python pre_deploy_backup.py restore <file>   - Restore from backup")
        print("  python pre_deploy_backup.py list             - List backups")
        print("")
        print("💡 Run 'backup' before each deployment to save current media files")
        return
    
    command = sys.argv[1].lower()
    
    if command == "backup":
        success = backup_production_media()
        if success:
            print("\n✅ Backup completed successfully!")
            print("💡 You can now safely deploy your changes")
        else:
            print("\n❌ Backup failed!")
            print("⚠️  Consider manual backup before deploying")
    
    elif command == "restore":
        if len(sys.argv) < 3:
            backups = list_backups()
            if backups:
                print(f"\nSpecify a backup file to restore:")
                print(f"  python pre_deploy_backup.py restore production_backups/{backups[0]}")
        else:
            backup_file = sys.argv[2]
            restore_media_backup(backup_file)
    
    elif command == "list":
        list_backups()
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()