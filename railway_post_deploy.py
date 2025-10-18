#!/usr/bin/env python3
"""
Post-deployment script for Railway
Automatically restores Digital Ocean URLs after deployment
"""
import os
import sys
import json
from pathlib import Path

# Add Django setup
sys.path.append('/app/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import django
django.setup()

def restore_from_latest_backup():
    """Find and restore from the latest backup"""
    backup_files = list(Path('.').glob('media_urls_backup_*.json'))
    if not backup_files:
        print("No backup files found")
        return
    
    latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
    print(f"Restoring from: {latest_backup}")
    
    # Import and run restore function
    from backup_restore_media_urls import restore_media_urls
    restore_media_urls(str(latest_backup))

if __name__ == "__main__":
    restore_from_latest_backup()
