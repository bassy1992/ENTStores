"""
Custom storage backends for ENTstore
Provides fallback storage options for media files
"""
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class PersistentFileSystemStorage(FileSystemStorage):
    """
    Enhanced FileSystemStorage that ensures files persist
    """
    
    def __init__(self, location=None, base_url=None):
        if location is None:
            # Use persistent disk location on Render
            if os.getenv('RENDER'):
                location = '/opt/render/project/data/media'
            else:
                location = os.path.join(settings.BASE_DIR, 'media')
        
        if base_url is None:
            base_url = settings.MEDIA_URL
        
        # Ensure directory exists
        os.makedirs(location, exist_ok=True)
        
        super().__init__(location, base_url)
    
    def _save(self, name, content):
        """Override save to ensure directory structure exists"""
        # Ensure the directory exists
        full_path = self.path(name)
        directory = os.path.dirname(full_path)
        os.makedirs(directory, exist_ok=True)
        
        # Call parent save
        saved_name = super()._save(name, content)
        
        # Create backup copy if on Render
        if os.getenv('RENDER'):
            self._create_backup_copy(saved_name)
        
        return saved_name
    
    def _create_backup_copy(self, name):
        """Create a backup copy of uploaded files"""
        try:
            source_path = self.path(name)
            backup_dir = '/opt/render/project/data/media_backup'
            os.makedirs(backup_dir, exist_ok=True)
            
            backup_path = os.path.join(backup_dir, name)
            backup_directory = os.path.dirname(backup_path)
            os.makedirs(backup_directory, exist_ok=True)
            
            import shutil
            shutil.copy2(source_path, backup_path)
            
        except Exception as e:
            # Don't fail the upload if backup fails
            print(f"Warning: Backup copy failed for {name}: {e}")
    
    def exists(self, name):
        """Check if file exists, with fallback to backup"""
        # Check primary location
        if super().exists(name):
            return True
        
        # Check backup location if on Render
        if os.getenv('RENDER'):
            backup_path = os.path.join('/opt/render/project/data/media_backup', name)
            if os.path.exists(backup_path):
                # Restore from backup
                self._restore_from_backup(name)
                return True
        
        return False
    
    def _restore_from_backup(self, name):
        """Restore file from backup location"""
        try:
            backup_path = os.path.join('/opt/render/project/data/media_backup', name)
            if os.path.exists(backup_path):
                primary_path = self.path(name)
                primary_directory = os.path.dirname(primary_path)
                os.makedirs(primary_directory, exist_ok=True)
                
                import shutil
                shutil.copy2(backup_path, primary_path)
                print(f"Restored {name} from backup")
                
        except Exception as e:
            print(f"Failed to restore {name} from backup: {e}")


class DualLocationStorage(PersistentFileSystemStorage):
    """
    Storage that maintains files in multiple locations for redundancy
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Additional storage locations for redundancy
        self.backup_locations = []
        
        if os.getenv('RENDER'):
            self.backup_locations = [
                '/opt/render/project/data/media_backup',
                '/opt/render/project/data/media_archive'
            ]
    
    def _save(self, name, content):
        """Save to primary location and all backup locations"""
        # Save to primary location
        saved_name = super()._save(name, content)
        
        # Save to backup locations
        for backup_location in self.backup_locations:
            try:
                backup_path = os.path.join(backup_location, saved_name)
                backup_directory = os.path.dirname(backup_path)
                os.makedirs(backup_directory, exist_ok=True)
                
                # Copy the saved file to backup location
                primary_path = self.path(saved_name)
                import shutil
                shutil.copy2(primary_path, backup_path)
                
            except Exception as e:
                print(f"Warning: Failed to backup to {backup_location}: {e}")
        
        return saved_name
    
    def exists(self, name):
        """Check existence in primary and backup locations"""
        # Check primary location first
        if super().exists(name):
            return True
        
        # Check backup locations and restore if found
        for backup_location in self.backup_locations:
            backup_path = os.path.join(backup_location, name)
            if os.path.exists(backup_path):
                try:
                    # Restore to primary location
                    primary_path = self.path(name)
                    primary_directory = os.path.dirname(primary_path)
                    os.makedirs(primary_directory, exist_ok=True)
                    
                    import shutil
                    shutil.copy2(backup_path, primary_path)
                    print(f"Auto-restored {name} from {backup_location}")
                    return True
                    
                except Exception as e:
                    print(f"Failed to restore {name} from {backup_location}: {e}")
        
        return False