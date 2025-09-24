from django.core.management.base import BaseCommand
from django.conf import settings
import os
import tarfile
import shutil
from datetime import datetime, timedelta
import requests
import json


class Command(BaseCommand):
    help = 'Comprehensive media backup and restore system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create backup of current media files',
        )
        parser.add_argument(
            '--restore',
            type=str,
            help='Restore from backup file',
        )
        parser.add_argument(
            '--auto-restore',
            action='store_true',
            help='Automatically restore from latest backup if media is missing',
        )
        parser.add_argument(
            '--download-from-url',
            type=str,
            help='Download and restore media from external URL',
        )
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Clean up old backup files',
        )

    def handle(self, *args, **options):
        self.backup_dir = '/opt/render/project/data/backups'
        self.media_dir = settings.MEDIA_ROOT
        
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)
        
        if options['backup']:
            self.create_backup()
        elif options['restore']:
            self.restore_backup(options['restore'])
        elif options['auto_restore']:
            self.auto_restore()
        elif options['download_from_url']:
            self.download_and_restore(options['download_from_url'])
        elif options['cleanup']:
            self.cleanup_old_backups()
        else:
            self.show_status()

    def create_backup(self):
        """Create a backup of current media files"""
        self.stdout.write("📦 Creating media backup...")
        
        if not os.path.exists(self.media_dir):
            self.stdout.write(self.style.WARNING("⚠️  Media directory doesn't exist"))
            return False
        
        # Count files
        file_count = sum(len(files) for _, _, files in os.walk(self.media_dir))
        if file_count == 0:
            self.stdout.write(self.style.WARNING("⚠️  No media files to backup"))
            return False
        
        # Create backup filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'media_backup_{timestamp}.tar.gz'
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        try:
            # Create tar.gz backup
            with tarfile.open(backup_path, 'w:gz') as tar:
                tar.add(self.media_dir, arcname='media')
            
            # Create metadata
            metadata = {
                'created': datetime.now().isoformat(),
                'file_count': file_count,
                'media_root': self.media_dir,
                'backup_size': os.path.getsize(backup_path)
            }
            
            metadata_path = backup_path.replace('.tar.gz', '_metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            size_mb = os.path.getsize(backup_path) / (1024 * 1024)
            self.stdout.write(self.style.SUCCESS(f"✅ Backup created: {backup_filename}"))
            self.stdout.write(f"📊 Files: {file_count}, Size: {size_mb:.1f} MB")
            
            return backup_path
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Backup failed: {e}"))
            return False

    def restore_backup(self, backup_file):
        """Restore media files from backup"""
        self.stdout.write(f"📥 Restoring from backup: {backup_file}")
        
        # Find backup file
        if not os.path.isabs(backup_file):
            backup_path = os.path.join(self.backup_dir, backup_file)
        else:
            backup_path = backup_file
        
        if not os.path.exists(backup_path):
            self.stdout.write(self.style.ERROR(f"❌ Backup file not found: {backup_path}"))
            return False
        
        try:
            # Clear existing media directory
            if os.path.exists(self.media_dir):
                shutil.rmtree(self.media_dir)
            
            # Create media directory
            os.makedirs(self.media_dir, exist_ok=True)
            
            # Extract backup
            with tarfile.open(backup_path, 'r:gz') as tar:
                # Extract to parent directory (since archive contains 'media' folder)
                tar.extractall(os.path.dirname(self.media_dir))
            
            # Count restored files
            file_count = sum(len(files) for _, _, files in os.walk(self.media_dir))
            
            self.stdout.write(self.style.SUCCESS(f"✅ Restored {file_count} files"))
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Restore failed: {e}"))
            return False

    def auto_restore(self):
        """Automatically restore from latest backup if media is missing"""
        self.stdout.write("🔄 Auto-restore: Checking media files...")
        
        # Check if media files are missing
        from shop.models import Product, Category
        
        missing_files = []
        
        for product in Product.objects.exclude(image=''):
            if product.image:
                full_path = os.path.join(self.media_dir, str(product.image))
                if not os.path.exists(full_path):
                    missing_files.append(str(product.image))
        
        for category in Category.objects.exclude(image=''):
            if category.image:
                full_path = os.path.join(self.media_dir, str(category.image))
                if not os.path.exists(full_path):
                    missing_files.append(str(category.image))
        
        if not missing_files:
            self.stdout.write(self.style.SUCCESS("✅ All media files present"))
            return True
        
        self.stdout.write(f"⚠️  Found {len(missing_files)} missing files")
        
        # Find latest backup
        latest_backup = self.get_latest_backup()
        if not latest_backup:
            self.stdout.write(self.style.ERROR("❌ No backups found for auto-restore"))
            return False
        
        self.stdout.write(f"🔄 Auto-restoring from: {latest_backup}")
        return self.restore_backup(latest_backup)

    def download_and_restore(self, url):
        """Download media backup from URL and restore"""
        self.stdout.write(f"🌐 Downloading backup from: {url}")
        
        try:
            import urllib.request
            
            # Download to temporary file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_file = os.path.join(self.backup_dir, f'downloaded_backup_{timestamp}.tar.gz')
            
            urllib.request.urlretrieve(url, temp_file)
            
            size_mb = os.path.getsize(temp_file) / (1024 * 1024)
            self.stdout.write(f"✅ Downloaded {size_mb:.1f} MB")
            
            # Restore from downloaded file
            success = self.restore_backup(temp_file)
            
            if success:
                # Keep the downloaded backup
                self.stdout.write(f"💾 Backup saved as: {os.path.basename(temp_file)}")
            else:
                # Remove failed download
                os.remove(temp_file)
            
            return success
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Download failed: {e}"))
            return False

    def get_latest_backup(self):
        """Get the latest backup file"""
        if not os.path.exists(self.backup_dir):
            return None
        
        backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.tar.gz')]
        if not backups:
            return None
        
        backups.sort(reverse=True)  # Most recent first
        return os.path.join(self.backup_dir, backups[0])

    def cleanup_old_backups(self, keep_count=5):
        """Clean up old backup files, keeping only the most recent ones"""
        self.stdout.write(f"🧹 Cleaning up old backups (keeping {keep_count})...")
        
        if not os.path.exists(self.backup_dir):
            return
        
        backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.tar.gz')]
        backups.sort(reverse=True)  # Most recent first
        
        removed_count = 0
        for backup in backups[keep_count:]:
            backup_path = os.path.join(self.backup_dir, backup)
            metadata_path = backup_path.replace('.tar.gz', '_metadata.json')
            
            try:
                os.remove(backup_path)
                if os.path.exists(metadata_path):
                    os.remove(metadata_path)
                removed_count += 1
                self.stdout.write(f"   🗑️  Removed: {backup}")
            except Exception as e:
                self.stdout.write(f"   ⚠️  Failed to remove {backup}: {e}")
        
        self.stdout.write(f"✅ Cleaned up {removed_count} old backups")

    def show_status(self):
        """Show current backup and media status"""
        self.stdout.write("📊 Media Backup System Status")
        self.stdout.write("=" * 40)
        
        # Media directory status
        if os.path.exists(self.media_dir):
            file_count = sum(len(files) for _, _, files in os.walk(self.media_dir))
            self.stdout.write(f"📁 Media directory: {self.media_dir}")
            self.stdout.write(f"📄 Media files: {file_count}")
        else:
            self.stdout.write(self.style.WARNING("⚠️  Media directory doesn't exist"))
        
        # Backup directory status
        if os.path.exists(self.backup_dir):
            backups = [f for f in os.listdir(self.backup_dir) if f.endswith('.tar.gz')]
            self.stdout.write(f"💾 Backup directory: {self.backup_dir}")
            self.stdout.write(f"📦 Available backups: {len(backups)}")
            
            if backups:
                backups.sort(reverse=True)
                latest = backups[0]
                latest_path = os.path.join(self.backup_dir, latest)
                size_mb = os.path.getsize(latest_path) / (1024 * 1024)
                self.stdout.write(f"🕒 Latest backup: {latest} ({size_mb:.1f} MB)")
        else:
            self.stdout.write(self.style.WARNING("⚠️  No backup directory found"))
        
        # Database status
        from shop.models import Product, Category
        products_with_images = Product.objects.exclude(image='').count()
        categories_with_images = Category.objects.exclude(image='').count()
        
        self.stdout.write(f"🛍️  Products with images: {products_with_images}")
        self.stdout.write(f"🏷️  Categories with images: {categories_with_images}")