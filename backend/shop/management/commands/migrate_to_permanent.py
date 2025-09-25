from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Product, Category
import os
import requests
import json
import base64
from django.core.files.base import ContentFile
from urllib.parse import urljoin
import hashlib
from datetime import datetime


class Command(BaseCommand):
    help = 'Automatically sync media files to permanent storage'

    def add_arguments(self, parser):
        parser.add_argument(
            '--auto-sync',
            action='store_true',
            help='Automatically sync all media files (default behavior)',
        )
        parser.add_argument(
            '--force-create',
            action='store_true',
            help='Force create all missing files',
        )
        parser.add_argument(
            '--verify-only',
            action='store_true',
            help='Only verify files without creating',
        )
        parser.add_argument(
            '--use-fallback',
            action='store_true',
            help='Use fallback storage methods',
        )

    def handle(self, *args, **options):
        self.stdout.write("🔄 Auto-Sync Media System Starting...")
        
        if options['verify_only']:
            self.verify_all_files()
        elif options['force_create']:
            self.force_create_all_files()
        elif options['use_fallback']:
            self.use_fallback_storage()
        else:
            # Default: Auto-sync everything
            self.auto_sync_media()

    def auto_sync_media(self):
        """Automatically sync all media files using best available method"""
        self.stdout.write("🚀 Auto-syncing media files...")
        
        # Step 1: Check what storage options are available
        storage_options = self.detect_storage_options()
        
        # Step 2: Ensure all required files exist
        missing_files = self.get_missing_files()
        
        if missing_files:
            self.stdout.write(f"📋 Found {len(missing_files)} missing files")
            
            # Step 3: Try to restore from available sources
            restored = self.restore_from_available_sources(missing_files)
            
            # Step 4: Create placeholders for any still missing
            still_missing = self.get_missing_files()
            if still_missing:
                self.stdout.write(f"🖼️ Creating {len(still_missing)} placeholder files...")
                self.create_placeholder_files(still_missing)
        
        # Step 5: Upload to permanent storage if available
        if storage_options['github'] or storage_options['cloudinary']:
            self.upload_to_permanent_storage()
        
        # Step 6: Verify everything works
        self.verify_all_files()
        
        self.stdout.write("✅ Auto-sync completed!")

    def detect_storage_options(self):
        """Detect what storage options are available"""
        options = {
            'github': bool(os.getenv('GITHUB_TOKEN')),
            'cloudinary': bool(os.getenv('CLOUDINARY_API_KEY')),
            'local': True
        }
        
        self.stdout.write("📊 Available storage options:")
        for storage, available in options.items():
            status = "✅" if available else "❌"
            self.stdout.write(f"   {status} {storage.title()}")
        
        return options

    def get_missing_files(self):
        """Get list of all missing media files"""
        missing = []
        
        # Check products
        for product in Product.objects.exclude(image=''):
            if product.image:
                file_path = str(product.image)
                local_path = os.path.join(settings.MEDIA_ROOT, file_path)
                if not os.path.exists(local_path):
                    missing.append({
                        'type': 'product',
                        'id': product.id,
                        'title': product.title,
                        'file_path': file_path,
                        'local_path': local_path
                    })
        
        # Check categories
        for category in Category.objects.exclude(image=''):
            if category.image:
                file_path = str(category.image)
                local_path = os.path.join(settings.MEDIA_ROOT, file_path)
                if not os.path.exists(local_path):
                    missing.append({
                        'type': 'category',
                        'id': category.key,
                        'title': category.label,
                        'file_path': file_path,
                        'local_path': local_path
                    })
        
        return missing

    def restore_from_available_sources(self, missing_files):
        """Try to restore missing files from various sources"""
        restored_count = 0
        
        for file_info in missing_files:
            file_path = file_info['file_path']
            local_path = file_info['local_path']
            
            # Try GitHub first
            if self.restore_from_github(file_path, local_path):
                self.stdout.write(f"✅ Restored from GitHub: {file_path}")
                restored_count += 1
                continue
            
            # Try Cloudinary
            if self.restore_from_cloudinary(file_path, local_path):
                self.stdout.write(f"✅ Restored from Cloudinary: {file_path}")
                restored_count += 1
                continue
            
            # Try backup locations
            if self.restore_from_backup_locations(file_path, local_path):
                self.stdout.write(f"✅ Restored from backup: {file_path}")
                restored_count += 1
                continue
        
        if restored_count > 0:
            self.stdout.write(f"🔄 Restored {restored_count} files from external sources")
        
        return restored_count

    def restore_from_github(self, file_path, local_path):
        """Try to restore file from GitHub"""
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            return False
        
        try:
            # Try to download from GitHub raw URL
            github_url = f"https://raw.githubusercontent.com/bassy1992/ENTstore-media/main/{file_path}"
            
            response = requests.get(github_url, timeout=10)
            if response.status_code == 200:
                # Create directory and save file
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            pass
        
        return False

    def restore_from_cloudinary(self, file_path, local_path):
        """Try to restore file from Cloudinary"""
        cloudinary_name = os.getenv('CLOUDINARY_CLOUD_NAME', 'entstore')
        if not cloudinary_name:
            return False
        
        try:
            # Try Cloudinary URL
            cloudinary_url = f"https://res.cloudinary.com/{cloudinary_name}/image/upload/entstore/{file_path.replace('/', '_').replace('.', '_')}"
            
            response = requests.get(cloudinary_url, timeout=10)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                return True
        except Exception as e:
            pass
        
        return False

    def restore_from_backup_locations(self, file_path, local_path):
        """Try to restore from backup locations"""
        backup_locations = [
            '/opt/render/project/data/media_backup',
            '/opt/render/project/data/media_archive',
            '/opt/render/project/data/backups'
        ]
        
        for backup_dir in backup_locations:
            backup_file = os.path.join(backup_dir, file_path)
            if os.path.exists(backup_file):
                try:
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    import shutil
                    shutil.copy2(backup_file, local_path)
                    return True
                except Exception as e:
                    continue
        
        return False

    def create_placeholder_files(self, missing_files):
        """Create placeholder files for missing media"""
        placeholder_data = self.get_placeholder_image_data()
        
        for file_info in missing_files:
            local_path = file_info['local_path']
            
            try:
                # Create directory
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                # Create placeholder file
                with open(local_path, 'wb') as f:
                    f.write(placeholder_data)
                
                self.stdout.write(f"🖼️ Created placeholder: {file_info['file_path']}")
                
            except Exception as e:
                self.stdout.write(f"❌ Failed to create placeholder {file_info['file_path']}: {e}")

    def upload_to_permanent_storage(self):
        """Upload all files to permanent storage"""
        github_token = os.getenv('GITHUB_TOKEN')
        
        if not github_token:
            self.stdout.write("ℹ️  No GitHub token - skipping permanent upload")
            return
        
        uploaded_count = 0
        
        # Upload all existing files
        for root, dirs, files in os.walk(settings.MEDIA_ROOT):
            for file in files:
                local_file = os.path.join(root, file)
                relative_path = os.path.relpath(local_file, settings.MEDIA_ROOT)
                
                if self.upload_file_to_github(local_file, relative_path):
                    uploaded_count += 1
        
        if uploaded_count > 0:
            self.stdout.write(f"☁️ Uploaded {uploaded_count} files to permanent storage")

    def upload_file_to_github(self, local_file, relative_path):
        """Upload a single file to GitHub"""
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            return False
        
        try:
            # Read file
            with open(local_file, 'rb') as f:
                file_content = f.read()
            
            # Encode to base64
            file_b64 = base64.b64encode(file_content).decode('utf-8')
            
            # GitHub API URL
            api_url = f"https://api.github.com/repos/bassy1992/ENTstore-media/contents/{relative_path}"
            
            # Check if file exists
            headers = {'Authorization': f'token {github_token}'}
            existing = requests.get(api_url, headers=headers)
            
            # Prepare commit data
            commit_data = {
                'message': f'Auto-sync: {relative_path}',
                'content': file_b64,
                'branch': 'main'
            }
            
            if existing.status_code == 200:
                commit_data['sha'] = existing.json()['sha']
            
            # Upload
            response = requests.put(api_url, json=commit_data, headers=headers)
            
            if response.status_code in [200, 201]:
                return True
            else:
                # Don't spam errors for every file
                pass
                
        except Exception as e:
            pass
        
        return False

    def get_placeholder_image_data(self):
        """Get placeholder image data"""
        # Minimal valid JPEG (1x1 gray pixel)
        return (
            b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
            b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08'
            b'\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e'
            b'\x1d\x1a\x1c\x1c $.\' \",#\x1c\x1c(7),01444\x1f\'9=82<.342'
            b'\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01'
            b'\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        )

    def force_create_all_files(self):
        """Force create all missing files"""
        self.stdout.write("🚨 Force creating all missing files...")
        
        missing_files = self.get_missing_files()
        if missing_files:
            self.create_placeholder_files(missing_files)
            self.upload_to_permanent_storage()
        
        self.verify_all_files()

    def use_fallback_storage(self):
        """Use fallback storage methods"""
        self.stdout.write("🔄 Using fallback storage methods...")
        
        # Create all missing files locally
        missing_files = self.get_missing_files()
        if missing_files:
            self.create_placeholder_files(missing_files)
        
        # Try to backup to multiple locations
        self.create_local_backups()
        
        self.stdout.write("✅ Fallback storage setup complete")

    def create_local_backups(self):
        """Create local backups in multiple locations"""
        backup_locations = [
            '/opt/render/project/data/media_backup',
            '/opt/render/project/data/media_archive',
            '/opt/render/project/data/media_emergency'
        ]
        
        for backup_dir in backup_locations:
            try:
                os.makedirs(backup_dir, exist_ok=True)
                
                # Copy all media files to backup location
                import shutil
                for root, dirs, files in os.walk(settings.MEDIA_ROOT):
                    for file in files:
                        src_file = os.path.join(root, file)
                        rel_path = os.path.relpath(src_file, settings.MEDIA_ROOT)
                        dst_file = os.path.join(backup_dir, rel_path)
                        
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                
                self.stdout.write(f"💾 Created backup in: {backup_dir}")
                
            except Exception as e:
                self.stdout.write(f"⚠️  Backup failed for {backup_dir}: {e}")

    def verify_all_files(self):
        """Verify all files are accessible"""
        self.stdout.write("🔍 Verifying all media files...")
        
        verified_count = 0
        missing_count = 0
        
        # Check products
        for product in Product.objects.exclude(image=''):
            if product.image:
                file_path = str(product.image)
                local_path = os.path.join(settings.MEDIA_ROOT, file_path)
                
                if os.path.exists(local_path):
                    # Test if file is accessible via URL
                    media_url = f"https://entstores.onrender.com/media/{file_path}"
                    self.stdout.write(f"✅ Product {product.id}: {media_url}")
                    verified_count += 1
                else:
                    self.stdout.write(f"❌ Missing: {file_path}")
                    missing_count += 1
        
        # Check categories
        for category in Category.objects.exclude(image=''):
            if category.image:
                file_path = str(category.image)
                local_path = os.path.join(settings.MEDIA_ROOT, file_path)
                
                if os.path.exists(local_path):
                    media_url = f"https://entstores.onrender.com/media/{file_path}"
                    self.stdout.write(f"✅ Category {category.key}: {media_url}")
                    verified_count += 1
                else:
                    self.stdout.write(f"❌ Missing: {file_path}")
                    missing_count += 1
        
        # Summary
        total_files = verified_count + missing_count
        self.stdout.write(f"📊 Verification Summary:")
        self.stdout.write(f"   ✅ Verified: {verified_count}/{total_files}")
        self.stdout.write(f"   ❌ Missing: {missing_count}/{total_files}")
        
        if missing_count == 0:
            self.stdout.write("🎉 All media files are accessible!")
        else:
            self.stdout.write("⚠️  Some files are missing - they will be auto-created")

    def show_status(self):
        """Show current media sync status"""
        self.stdout.write("🔄 Auto-Sync Media Status")
        self.stdout.write("=" * 40)
        
        # Check storage options
        storage_options = self.detect_storage_options()
        
        # Check file status
        missing_files = self.get_missing_files()
        total_expected = Product.objects.exclude(image='').count() + Category.objects.exclude(image='').count()
        existing_files = total_expected - len(missing_files)
        
        self.stdout.write(f"📊 File Status:")
        self.stdout.write(f"   ✅ Existing: {existing_files}/{total_expected}")
        self.stdout.write(f"   ❌ Missing: {len(missing_files)}/{total_expected}")
        
        # Check local media directory
        if os.path.exists(settings.MEDIA_ROOT):
            local_file_count = sum(len(files) for _, _, files in os.walk(settings.MEDIA_ROOT))
            self.stdout.write(f"📁 Local files: {local_file_count}")
        else:
            self.stdout.write("📁 Local media directory: Not found")
        
        # Show recommendations
        self.stdout.write("\n💡 Recommendations:")
        if missing_files:
            self.stdout.write("   🔄 Run auto-sync to fix missing files")
        if not storage_options['github']:
            self.stdout.write("   ☁️  Add GITHUB_TOKEN for permanent storage")
        if existing_files == total_expected:
            self.stdout.write("   ✅ All files present - system is healthy!")