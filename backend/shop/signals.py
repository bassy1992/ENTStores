"""
Django signals for automatic media URL management
"""
import os
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


@receiver(post_migrate)
def restore_media_urls_after_migrate(sender, **kwargs):
    """
    Automatically restore media URLs after migrations
    This ensures URLs are restored even if the auto_restore app doesn't run
    """
    # Only run for the shop app and only in production
    if sender.name == 'shop' and os.getenv('RAILWAY_ENVIRONMENT'):
        try:
            # Import here to avoid circular imports
            from .media_url_constants import restore_all_media_urls
            
            restored_count = restore_all_media_urls()
            print(f"🔄 Post-migration: Restored {restored_count} media URLs")
            
        except ImportError:
            print("⚠️  Media URL constants not found - run railway_permanent_media_setup.py")
        except Exception as e:
            print(f"⚠️  Post-migration restore failed: {e}")


@receiver(post_migrate)
def update_media_url_constants(sender, **kwargs):
    """
    Update media URL constants file when new URLs are added
    This keeps the constants file in sync with the database
    """
    if sender.name == 'shop':
        try:
            # Only update if we're not in Railway (to avoid overwriting during deployment)
            if not os.getenv('RAILWAY_ENVIRONMENT'):
                from .models import Product, Category, ProductImage
                
                # Check if there are new URLs that aren't in constants
                try:
                    from .media_url_constants import MEDIA_URLS
                    
                    # Count current URLs in database
                    db_product_urls = Product.objects.filter(image_url__isnull=False).exclude(image_url='').count()
                    db_category_urls = Category.objects.filter(image_url__isnull=False).exclude(image_url='').count()
                    db_image_urls = ProductImage.objects.filter(image_url__isnull=False).exclude(image_url='').count()
                    
                    total_db_urls = db_product_urls + db_category_urls + db_image_urls
                    total_constant_urls = len(MEDIA_URLS)
                    
                    if total_db_urls > total_constant_urls:
                        print(f"📊 Found {total_db_urls - total_constant_urls} new media URLs")
                        print("💡 Run 'python railway_permanent_media_setup.py' to update constants")
                        
                except ImportError:
                    # Constants file doesn't exist yet
                    pass
                    
        except Exception as e:
            # Don't let signal errors break migrations
            pass