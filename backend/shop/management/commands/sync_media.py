from django.core.management.base import BaseCommand
from django.conf import settings
import os
import shutil


class Command(BaseCommand):
    help = 'Sync media files between local and persistent storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to-persistent',
            action='store_true',
            help='Copy from local media to persistent disk',
        )
        parser.add_argument(
            '--from-persistent',
            action='store_true',
            help='Copy from persistent disk to local media',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be copied without actually copying',
        )

    def handle(self, *args, **options):
        if not os.getenv('RENDER'):
            self.stdout.write(self.style.WARNING('⚠️  Not running on Render, skipping sync'))
            return

        persistent_media = '/opt/render/project/data/media'
        local_media = os.path.join(settings.BASE_DIR, 'media')
        
        self.stdout.write(f"📁 Persistent media: {persistent_media}")
        self.stdout.write(f"📁 Local media: {local_media}")
        self.stdout.write(f"📁 Settings MEDIA_ROOT: {settings.MEDIA_ROOT}")
        
        # Ensure both directories exist
        os.makedirs(persistent_media, exist_ok=True)
        os.makedirs(local_media, exist_ok=True)
        
        if options['to_persistent']:
            self.sync_directories(local_media, persistent_media, options['dry_run'])
        elif options['from_persistent']:
            self.sync_directories(persistent_media, local_media, options['dry_run'])
        else:
            # Default: sync both ways, prioritizing persistent storage
            self.stdout.write("🔄 Syncing media files (bidirectional)...")
            
            # First, copy any new files from local to persistent
            local_files = self.get_file_list(local_media)
            persistent_files = self.get_file_list(persistent_media)
            
            self.stdout.write(f"📊 Local files: {len(local_files)}")
            self.stdout.write(f"📊 Persistent files: {len(persistent_files)}")
            
            # Copy newer files from local to persistent
            copied_to_persistent = self.sync_directories(local_media, persistent_media, options['dry_run'], check_newer=True)
            
            # Copy newer files from persistent to local
            copied_to_local = self.sync_directories(persistent_media, local_media, options['dry_run'], check_newer=True)
            
            self.stdout.write(self.style.SUCCESS(f"✅ Sync completed: {copied_to_persistent} to persistent, {copied_to_local} to local"))

    def get_file_list(self, directory):
        """Get list of all files in directory"""
        files = []
        if os.path.exists(directory):
            for root, dirs, filenames in os.walk(directory):
                for filename in filenames:
                    rel_path = os.path.relpath(os.path.join(root, filename), directory)
                    files.append(rel_path)
        return files

    def sync_directories(self, source, destination, dry_run=False, check_newer=False):
        """Sync files from source to destination"""
        copied_count = 0
        
        if not os.path.exists(source):
            self.stdout.write(self.style.WARNING(f"⚠️  Source directory doesn't exist: {source}"))
            return copied_count
        
        self.stdout.write(f"🔄 Syncing {source} -> {destination}")
        
        for root, dirs, files in os.walk(source):
            for file in files:
                source_file = os.path.join(root, file)
                rel_path = os.path.relpath(source_file, source)
                dest_file = os.path.join(destination, rel_path)
                
                # Create destination directory if it doesn't exist
                dest_dir = os.path.dirname(dest_file)
                if not dry_run:
                    os.makedirs(dest_dir, exist_ok=True)
                
                should_copy = True
                
                if check_newer and os.path.exists(dest_file):
                    source_mtime = os.path.getmtime(source_file)
                    dest_mtime = os.path.getmtime(dest_file)
                    should_copy = source_mtime > dest_mtime
                
                if should_copy:
                    if dry_run:
                        self.stdout.write(f"   📄 Would copy: {rel_path}")
                    else:
                        try:
                            shutil.copy2(source_file, dest_file)
                            self.stdout.write(f"   ✅ Copied: {rel_path}")
                            copied_count += 1
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"   ❌ Failed to copy {rel_path}: {e}"))
        
        return copied_count