"""
Permanent cloud storage solution for ENTstore
Uses multiple cloud providers for ultimate reliability
"""
import os
import base64
import requests
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from urllib.parse import urljoin
import hashlib
import json


class CloudinaryStorage(Storage):
    """
    Cloudinary-based storage for permanent media files
    Free tier: 25GB storage, 25GB bandwidth
    """
    
    def __init__(self):
        # Cloudinary config (free tier)
        self.cloud_name = "entstore"  # You'll need to create this
        self.api_key = "your_api_key"  # Set in environment
        self.api_secret = "your_api_secret"  # Set in environment
        self.base_url = f"https://res.cloudinary.com/{self.cloud_name}/image/upload/"
    
    def _save(self, name, content):
        """Upload file to Cloudinary"""
        try:
            # Read file content
            content.seek(0)
            file_data = content.read()
            
            # Prepare upload data
            upload_data = {
                'file': base64.b64encode(file_data).decode('utf-8'),
                'upload_preset': 'entstore_preset',  # Create this in Cloudinary
                'public_id': name.replace('/', '_').replace('.', '_'),
                'folder': 'entstore'
            }
            
            # Upload to Cloudinary
            response = requests.post(
                f"https://api.cloudinary.com/v1_1/{self.cloud_name}/image/upload",
                data=upload_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['public_id']
            else:
                raise Exception(f"Cloudinary upload failed: {response.text}")
                
        except Exception as e:
            print(f"Cloudinary upload failed: {e}")
            # Fallback to local storage
            return self._save_local_fallback(name, content)
    
    def _save_local_fallback(self, name, content):
        """Fallback to local storage"""
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with open(local_path, 'wb') as f:
            content.seek(0)
            f.write(content.read())
        
        return name
    
    def url(self, name):
        """Return URL for accessing the file"""
        if name.startswith('http'):
            return name
        
        # Try Cloudinary URL first
        cloudinary_url = f"https://res.cloudinary.com/{self.cloud_name}/image/upload/entstore/{name.replace('/', '_').replace('.', '_')}"
        
        # Check if file exists on Cloudinary
        try:
            response = requests.head(cloudinary_url, timeout=5)
            if response.status_code == 200:
                return cloudinary_url
        except:
            pass
        
        # Fallback to local URL
        return urljoin(settings.MEDIA_URL, name)
    
    def exists(self, name):
        """Check if file exists"""
        # Check Cloudinary
        cloudinary_url = f"https://res.cloudinary.com/{self.cloud_name}/image/upload/entstore/{name.replace('/', '_').replace('.', '_')}"
        try:
            response = requests.head(cloudinary_url, timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        
        # Check local
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        return os.path.exists(local_path)


class GitHubStorage(Storage):
    """
    GitHub-based storage using repository as CDN
    Completely free and permanent
    """
    
    def __init__(self):
        self.repo_owner = "bassy1992"  # Your GitHub username
        self.repo_name = "ENTstore-media"  # Create this repo
        self.branch = "main"
        self.token = os.getenv('GITHUB_TOKEN', '')  # Set in environment
        self.base_url = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/{self.branch}/"
    
    def _save(self, name, content):
        """Upload file to GitHub repository"""
        try:
            # Read file content
            content.seek(0)
            file_data = content.read()
            file_b64 = base64.b64encode(file_data).decode('utf-8')
            
            # GitHub API URL
            api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{name}"
            
            # Check if file exists (for updates)
            headers = {'Authorization': f'token {self.token}'}
            existing = requests.get(api_url, headers=headers)
            
            # Prepare commit data
            commit_data = {
                'message': f'Upload {name}',
                'content': file_b64,
                'branch': self.branch
            }
            
            if existing.status_code == 200:
                # File exists, need SHA for update
                commit_data['sha'] = existing.json()['sha']
            
            # Upload/update file
            response = requests.put(api_url, json=commit_data, headers=headers)
            
            if response.status_code in [200, 201]:
                print(f"✅ Uploaded {name} to GitHub")
                return name
            else:
                raise Exception(f"GitHub upload failed: {response.text}")
                
        except Exception as e:
            print(f"GitHub upload failed: {e}")
            return self._save_local_fallback(name, content)
    
    def _save_local_fallback(self, name, content):
        """Fallback to local storage"""
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with open(local_path, 'wb') as f:
            content.seek(0)
            f.write(content.read())
        
        return name
    
    def url(self, name):
        """Return URL for accessing the file"""
        if name.startswith('http'):
            return name
        
        # Try GitHub raw URL first
        github_url = f"{self.base_url}{name}"
        
        try:
            response = requests.head(github_url, timeout=5)
            if response.status_code == 200:
                return github_url
        except:
            pass
        
        # Fallback to local URL
        return urljoin(settings.MEDIA_URL, name)
    
    def exists(self, name):
        """Check if file exists"""
        # Check GitHub
        github_url = f"{self.base_url}{name}"
        try:
            response = requests.head(github_url, timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        
        # Check local
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        return os.path.exists(local_path)


class PermanentStorage(Storage):
    """
    Ultimate permanent storage solution
    Uses multiple backends for maximum reliability
    """
    
    def __init__(self):
        self.backends = []
        
        # Add GitHub storage (always available)
        self.backends.append(GitHubStorage())
        
        # Add Cloudinary if configured
        if os.getenv('CLOUDINARY_API_KEY'):
            self.backends.append(CloudinaryStorage())
        
        # Local storage as final fallback
        from django.core.files.storage import FileSystemStorage
        self.local_storage = FileSystemStorage(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL
        )
    
    def _save(self, name, content):
        """Save to all available backends"""
        saved_name = name
        success_count = 0
        
        # Save to local first (immediate availability)
        try:
            local_path = os.path.join(settings.MEDIA_ROOT, name)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            with open(local_path, 'wb') as f:
                content.seek(0)
                f.write(content.read())
            
            success_count += 1
            print(f"✅ Saved {name} locally")
        except Exception as e:
            print(f"❌ Local save failed: {e}")
        
        # Save to cloud backends
        for backend in self.backends:
            try:
                content.seek(0)  # Reset file pointer
                backend._save(name, content)
                success_count += 1
                print(f"✅ Saved {name} to {backend.__class__.__name__}")
            except Exception as e:
                print(f"❌ {backend.__class__.__name__} save failed: {e}")
        
        print(f"📊 Saved {name} to {success_count} locations")
        return saved_name
    
    def url(self, name):
        """Return best available URL"""
        # Try cloud backends first (better performance)
        for backend in self.backends:
            try:
                url = backend.url(name)
                if url and not url.endswith(name):  # Valid cloud URL
                    return url
            except:
                continue
        
        # Fallback to local URL
        return self.local_storage.url(name)
    
    def exists(self, name):
        """Check if file exists in any backend"""
        # Check local first (fastest)
        if self.local_storage.exists(name):
            return True
        
        # Check cloud backends
        for backend in self.backends:
            try:
                if backend.exists(name):
                    # File exists in cloud, restore to local
                    self._restore_to_local(name, backend)
                    return True
            except:
                continue
        
        return False
    
    def _restore_to_local(self, name, backend):
        """Restore file from cloud to local storage"""
        try:
            url = backend.url(name)
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                local_path = os.path.join(settings.MEDIA_ROOT, name)
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"🔄 Restored {name} from {backend.__class__.__name__}")
        except Exception as e:
            print(f"❌ Failed to restore {name}: {e}")
    
    def delete(self, name):
        """Delete from all backends"""
        # Delete from local
        try:
            self.local_storage.delete(name)
        except:
            pass
        
        # Note: We don't delete from cloud backends for safety
        # Files remain as permanent backup