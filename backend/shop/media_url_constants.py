"""
Media URL Constants - Auto-generated on 2025-10-18T19:18:30.043809
This file contains all media URLs as constants to preserve them across deployments
"""

# Media URL constants
MEDIA_URLS = {
    "PRODUCT_jeans-001": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop",
    "PRODUCT_hoodie-001": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop",
    "PRODUCT_tshirt-001": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop",
    "PRODUCT_ent-tracksuit-001": "https://images.unsplash.com/photo-1506629905607-d9f02a6a0e7b?w=400&h=400&fit=crop&crop=center",
    "PRODUCT_ent-cap-001": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=400&fit=crop&crop=center",
    "PRODUCT_ent-shorts-001": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&h=400&fit=crop&crop=center",
    "PRODUCT_ent-jacket-001": "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop&crop=center",
    "PRODUCT_ent-polo-001": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop&crop=center",
    "PRODUCT_ent-hoodie-001": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop&crop=center",
    "PRODUCT_ent-tshirt-002": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&h=400&fit=crop&crop=center",
    "PRODUCT_ent-tshirt-001": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center",
    "PRODIMG_1": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center",
    "PRODIMG_2": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&h=400&fit=crop&crop=center",
    "PRODIMG_4": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center",
    "PRODIMG_3": "https://images.unsplash.com/photo-1583743814966-8936f37f4678?w=400&h=400&fit=crop&crop=center",
    "PRODIMG_5": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&h=400&fit=crop&crop=center",
    "PRODIMG_6": "https://images.unsplash.com/photo-1583743814966-8936f37f4678?w=400&h=400&fit=crop&crop=center",
    "PRODIMG_7": "https://images.unsplash.com/photo-1571945153237-4929e783af4a?w=400&h=400&fit=crop&crop=center",
    "PRODIMG_8": "https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400&h=400&fit=crop&crop=center",

}

def get_product_image_url(product_id):
    """Get product image URL by product ID"""
    return MEDIA_URLS.get(f"PRODUCT_{product_id}")

def get_category_image_url(category_key):
    """Get category image URL by category key"""
    return MEDIA_URLS.get(f"CATEGORY_{category_key}")

def get_product_image_by_id(image_id):
    """Get product image URL by image ID"""
    return MEDIA_URLS.get(f"PRODIMG_{image_id}")

def restore_all_media_urls():
    """Restore all media URLs to database"""
    from shop.models import Product, Category, ProductImage
    
    restored_count = 0
    
    # Restore product URLs
    for key, url in MEDIA_URLS.items():
        if key.startswith("PRODUCT_"):
            product_id = key.replace("PRODUCT_", "")
            try:
                product = Product.objects.get(id=product_id)
                if not product.image_url:
                    product.image_url = url
                    product.save(update_fields=['image_url'])
                    restored_count += 1
            except Product.DoesNotExist:
                pass
        
        elif key.startswith("CATEGORY_"):
            category_key = key.replace("CATEGORY_", "")
            try:
                category = Category.objects.get(key=category_key)
                if not category.image_url:
                    category.image_url = url
                    category.save(update_fields=['image_url'])
                    restored_count += 1
            except Category.DoesNotExist:
                pass
        
        elif key.startswith("PRODIMG_"):
            img_id = key.replace("PRODIMG_", "")
            try:
                img = ProductImage.objects.get(id=img_id)
                if not img.image_url:
                    img.image_url = url
                    img.save(update_fields=['image_url'])
                    restored_count += 1
            except ProductImage.DoesNotExist:
                pass
    
    return restored_count
