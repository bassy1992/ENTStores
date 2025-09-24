#!/usr/bin/env python
"""
Media Guardian - Monitors and protects media files
Runs continuously to ensure media files are always available
"""
import os
import time
import sys
import django
from datetime import datetime, timedelta

# Setup Django
sys.path.insert(0, '/opt/render/project/src/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.conf import settings
from shop.models import Product, Category

class MediaGuardian:
    def __init__(self):
        self.media_root = settings.MEDIA_ROOT
        self.backup_dir = '/opt/render/project/data/backups'
        self.check_interval = 300  # 5 minutes
        self.last_backup = None
        
    def check_media_integrity(self):
        """Check if all referenced media files exist"""
        missing_files = []
        
        # Check products
        for product in Product.objects.exclude(image=''):
            if product.image:
                full_path = os.path.join(self.media_root, str(product.image))
                if not os.path.exists(full_path):
                    missing_files.append(f"Product {product.id}: {product.image}")
        
        # Check categories
        for category in Category.objects.exclude(image=''):
            if category.image:
                full_path = os.path.join(self.media_root, str(category.image))
                if not os.path.exists(full_path):
                    missing_files.append(f"Category {category.key}: {category.image}")
        
        return missing_files
    
    def auto_restore_if_needed(self):
        """Automatically restore missing files"""
        missing = self.check_media_integrity()
        
        if missing:
            print(f"⚠️  {datetime.now()}: Found {len(missing)} missing files")
            for missing_file in missing[:5]:  # Show first 5
                print(f"   - {missing_file}")
            
            # Try to restore from latest backup
            latest_backup = self.get_latest_backup()
            if latest_backup:
                print(f"🔄 Auto-restoring from: {latest_backup}")
                success = self.restore_from_backup(latest_backup)
                if success:
                    print("✅ Auto-restore completed")
                    return True
                else:
                    print("❌ Auto-restore failed")
            else:
                print("❌ No backups available for restore")
        
        return False
    
    def get_latest_backup(self):
        """Get the most recent backup file"""
        if not os.path.exists(self.backup_dir):
            return None
        
        backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.tar.gz')]
        if not backups:
            return None
        
        backups.sort(reverse=True)
        return os.path.join(self.backup_dir, backups[0])
    
    def restore_from_backup(self, backup_path):
        """Restore media files from backup"""
        try:
            import subprocess
            result = subprocess.run([
                'python', '/opt/render/project/src/backend/manage.py',
                'backup_restore_media', '--restore', backup_path
            ], capture_output=True, text=True, cwd='/opt/render/project/src/backend')
            
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Restore error: {e}")
            return False
    
    def create_backup_if_needed(self):
        """Create backup if it's been a while since last one"""
        now = datetime.now()
        
        # Create backup every 6 hours
        if self.last_backup is None or (now - self.last_backup) > timedelta(hours=6):
            try:
                import subprocess
                result = subprocess.run([
                    'python', '/opt/render/project/src/backend/manage.py',
                    'backup_restore_media', '--backup'
                ], capture_output=True, text=True, cwd='/opt/render/project/src/backend')
                
                if result.returncode == 0:
                    self.last_backup = now
                    print(f"✅ {now}: Periodic backup created")
                else:
                    print(f"⚠️  {now}: Backup failed")
            except Exception as e:
                print(f"❌ {now}: Backup error: {e}")
    
    def run_guardian(self):
        """Main guardian loop"""
        print(f"🛡️  Media Guardian started at {datetime.now()}")
        print(f"📁 Monitoring: {self.media_root}")
        print(f"💾 Backups: {self.backup_dir}")
        print(f"⏰ Check interval: {self.check_interval} seconds")
        
        while True:
            try:
                # Check media integrity
                missing = self.check_media_integrity()
                
                if missing:
                    # Try to restore
                    self.auto_restore_if_needed()
                else:
                    # All good, maybe create periodic backup
                    self.create_backup_if_needed()
                
                # Wait before next check
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print(f"\n🛑 Media Guardian stopped at {datetime.now()}")
                break
            except Exception as e:
                print(f"❌ {datetime.now()}: Guardian error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--daemon':
        # Run as daemon
        guardian = MediaGuardian()
        guardian.run_guardian()
    else:
        # Single check
        guardian = MediaGuardian()
        missing = guardian.check_media_integrity()
        
        if missing:
            print(f"⚠️  Found {len(missing)} missing files:")
            for missing_file in missing:
                print(f"   - {missing_file}")
            
            # Try auto-restore
            guardian.auto_restore_if_needed()
        else:
            print("✅ All media files present")

if __name__ == "__main__":
    main()