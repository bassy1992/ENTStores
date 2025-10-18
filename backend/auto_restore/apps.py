"""
Auto-restore media URLs app
This app automatically restores media URLs when Django starts
"""
from django.apps import AppConfig

class AutoRestoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auto_restore'
    
    def ready(self):
        """Called when Django is ready - restore media URLs"""
        try:
            # Import here to avoid circular imports
            from shop.media_url_constants import restore_all_media_urls
            
            # Only restore if we're in production (Railway)
            import os
            if os.getenv('RAILWAY_ENVIRONMENT'):
                restored_count = restore_all_media_urls()
                print(f"🔄 Auto-restored {restored_count} media URLs")
        except Exception as e:
            print(f"⚠️  Auto-restore failed: {e}")
