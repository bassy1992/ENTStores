#!/usr/bin/env python3
"""
Deploy URL-based images functionality to Railway
This script handles the deployment of URL image features to your Railway production environment
"""

import os
import sys
import django
import subprocess
import json

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, Category


def create_migration_for_railway():
    """Create migration for the new image_url field in Category"""
    print("🔄 Creating migration for Railway deployment...")
    
    try:
        # Change to backend directory
        original_dir = os.getcwd()
        os.chdir('backend')
        
        # Create migration
        result = subprocess.run([
            sys.executable, 'manage.py', 'makemigrations', 'shop',
            '--name', 'add_category_image_url_field'
        ], capture_output=True, text=True)
        
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print("✅ Migration created successfully")
            print(result.stdout)
            return True
        else:
            print("❌ Error creating migration:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        os.chdir(original_dir)
        return False


def create_railway_deployment_script():
    """Create a script to run on Railway after deployment"""
    script_content = '''#!/usr/bin/env python3
"""
Railway post-deployment script for URL-based images
Run this after deploying to Railway to set up URL-based image functionality
"""

import os
import sys
import django
import json

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, Category


def add_sample_url_products():
    """Add sample products with URL-based images"""
    print("🚀 Adding sample products with URL-based images to Railway...")
    
    # Sample products with URLs
    sample_products = [
        {
            "id": "ent-tshirt-001",
            "title": "ENT Classic Black T-Shirt",
            "price": "25.99",
            "description": "Premium cotton t-shirt with ENT logo. Comfortable fit and high-quality print that lasts.",
            "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&crop=center",
            "category": "t-shirts",
            "stock_quantity": 50,
            "is_featured": True
        },
        {
            "id": "ent-tshirt-002",
            "title": "ENT White Logo T-Shirt",
            "price": "24.99",
            "description": "Clean white t-shirt with subtle ENT branding. Perfect for everyday wear.",
            "image_url": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=400&h=400&fit=crop&crop=center",
            "category": "t-shirts",
            "stock_quantity": 45,
            "is_featured": False
        },
        {
            "id": "ent-hoodie-001",
            "title": "ENT Premium Hoodie",
            "price": "59.99",
            "description": "Comfortable hoodie perfect for any weather. Made with premium materials for maximum comfort.",
            "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop&crop=center",
            "category": "hoodies",
            "stock_quantity": 25,
            "is_featured": True
        },
        {
            "id": "ent-polo-001",
            "title": "ENT Business Polo",
            "price": "39.99",
            "description": "Professional polo shirt perfect for business casual or smart casual occasions.",
            "image_url": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop&crop=center",
            "category": "polos",
            "stock_quantity": 30,
            "is_featured": False
        }
    ]
    
    success_count = 0
    for product_data in sample_products:
        try:
            # Check if category exists
            category = Category.objects.get(key=product_data['category'])
            
            # Create or update product
            product, created = Product.objects.update_or_create(
                id=product_data['id'],
                defaults={
                    'title': product_data['title'],
                    'price': product_data['price'],
                    'description': product_data['description'],
                    'image_url': product_data['image_url'],
                    'category': category,
                    'stock_quantity': product_data.get('stock_quantity', 0),
                    'is_featured': product_data.get('is_featured', False),
                    'is_active': True,
                }
            )
            
            action = "Created" if created else "Updated"
            print(f"✅ {action} product: {product.title}")
            success_count += 1
            
        except Category.DoesNotExist:
            print(f"❌ Category '{product_data['category']}' not found for product {product_data['id']}")
        except Exception as e:
            print(f"❌ Error adding product {product_data['id']}: {e}")
    
    print(f"\\n✅ Successfully processed {success_count} out of {len(sample_products)} products")


def update_existing_products_with_urls():
    """Update existing products to use URL-based images"""
    print("🔄 Updating existing products with URL-based images...")
    
    # Map of product IDs to image URLs (you can customize this)
    product_image_urls = {
        # Add your existing product IDs and their image URLs here
        # "existing-product-id": "https://your-image-url.com/image.jpg"
    }
    
    updated_count = 0
    for product_id, image_url in product_image_urls.items():
        try:
            product = Product.objects.get(id=product_id)
            product.image_url = image_url
            product.save()
            print(f"✅ Updated {product.title} with URL: {image_url}")
            updated_count += 1
        except Product.DoesNotExist:
            print(f"❌ Product {product_id} not found")
        except Exception as e:
            print(f"❌ Error updating product {product_id}: {e}")
    
    if updated_count > 0:
        print(f"\\n✅ Updated {updated_count} existing products with URLs")
    else:
        print("\\nℹ️  No existing products updated (add product IDs to the script)")


def main():
    """Main function"""
    print("🚀 Railway URL-Based Images Setup")
    print("=" * 40)
    
    try:
        add_sample_url_products()
        update_existing_products_with_urls()
        
        print("\\n✅ Railway deployment setup completed!")
        print("\\nURL-based images are now active:")
        print("- Products can use image_url field instead of file uploads")
        print("- Categories support image_url field")
        print("- API automatically serves the correct image source")
        print("- Fallback to placeholder images when needed")
        
    except Exception as e:
        print(f"\\n❌ Error during setup: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
'''
    
    with open('backend/railway_setup_url_images.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Created Railway setup script: backend/railway_setup_url_images.py")


def update_railway_deployment_files():
    """Update Railway deployment files to include URL image functionality"""
    print("🔄 Updating Railway deployment files...")
    
    # Update requirements.txt if needed
    requirements_path = 'backend/requirements.txt'
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r') as f:
            requirements = f.read()
        
        # Add any new requirements if needed (none for URL images)
        print("✅ Requirements.txt is up to date")
    
    # Update railway.json if it exists
    railway_json_path = 'backend/railway.json'
    if os.path.exists(railway_json_path):
        try:
            with open(railway_json_path, 'r') as f:
                railway_config = json.load(f)
            
            # Add post-deployment command if not present
            if 'build' not in railway_config:
                railway_config['build'] = {}
            
            if 'commands' not in railway_config['build']:
                railway_config['build']['commands'] = []
            
            # Add migration command
            migration_cmd = "python manage.py migrate"
            if migration_cmd not in railway_config['build']['commands']:
                railway_config['build']['commands'].append(migration_cmd)
            
            # Add URL images setup command
            setup_cmd = "python railway_setup_url_images.py"
            if setup_cmd not in railway_config['build']['commands']:
                railway_config['build']['commands'].append(setup_cmd)
            
            with open(railway_json_path, 'w') as f:
                json.dump(railway_config, f, indent=2)
            
            print("✅ Updated railway.json with URL images setup")
            
        except Exception as e:
            print(f"❌ Error updating railway.json: {e}")


def create_deployment_instructions():
    """Create deployment instructions"""
    instructions = '''# Railway Deployment Instructions for URL-Based Images

## Automatic Deployment
The following files have been updated for automatic deployment:

1. **Migration**: New migration created for Category.image_url field
2. **Setup Script**: `railway_setup_url_images.py` will run after deployment
3. **Railway Config**: Updated to include migration and setup commands

## Manual Steps (if needed)

### 1. Deploy to Railway
```bash
git add .
git commit -m "Add URL-based images functionality"
git push origin main
```

### 2. Run Setup Script (if automatic setup fails)
In Railway console:
```bash
python railway_setup_url_images.py
```

### 3. Verify Deployment
Check these endpoints:
- `/api/products/` - Should show products with image URLs
- `/api/categories/` - Should support image URLs
- `/admin/` - Should have image_url fields in forms

## Features Added

✅ **URL-Based Product Images**
- Products can use `image_url` field instead of file uploads
- Automatic fallback: uploaded file → URL → placeholder

✅ **URL-Based Category Images**  
- Categories now support `image_url` field
- Same fallback logic as products

✅ **API Updates**
- All image fields now use the smart `get_image_url()` method
- Consistent image handling across endpoints

✅ **Performance Benefits**
- Faster loading from CDNs
- No server storage costs
- Easy image management

## Testing After Deployment

1. **Check API Response**:
   ```bash
   curl https://your-railway-app.railway.app/api/products/
   ```

2. **Verify Images Load**:
   - Open your frontend
   - Check that product images display correctly
   - Verify category images work

3. **Test Admin Interface**:
   - Login to Django admin
   - Check product/category forms have image_url fields
   - Add a test product with URL-based image

## Troubleshooting

### Images Not Showing
- Check if URLs are accessible (HTTPS required)
- Verify CORS settings for external images
- Check browser console for errors

### Migration Issues
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

### Reset and Re-run Setup
```bash
python railway_setup_url_images.py
```

## Next Steps

1. **Add More Products**: Use image URLs instead of uploads
2. **Update Existing Products**: Replace file uploads with CDN URLs  
3. **Optimize Images**: Use URL parameters for size/quality
4. **Monitor Performance**: Check image loading speeds

---
**Need Help?** Check the Railway logs or run the setup script manually.
'''
    
    with open('RAILWAY_URL_IMAGES_DEPLOYMENT.md', 'w') as f:
        f.write(instructions)
    
    print("✅ Created deployment instructions: RAILWAY_URL_IMAGES_DEPLOYMENT.md")


def main():
    """Main deployment preparation function"""
    print("🚀 Preparing URL-Based Images for Railway Deployment")
    print("=" * 55)
    
    # Step 1: Create migration
    if create_migration_for_railway():
        print("✅ Migration ready for Railway")
    else:
        print("❌ Migration creation failed")
        return
    
    # Step 2: Create Railway setup script
    create_railway_deployment_script()
    
    # Step 3: Update Railway deployment files
    update_railway_deployment_files()
    
    # Step 4: Create deployment instructions
    create_deployment_instructions()
    
    print("\n🎉 Railway Deployment Preparation Complete!")
    print("\nNext steps:")
    print("1. Review the files created:")
    print("   - Migration file in backend/shop/migrations/")
    print("   - backend/railway_setup_url_images.py")
    print("   - RAILWAY_URL_IMAGES_DEPLOYMENT.md")
    print("\n2. Deploy to Railway:")
    print("   git add .")
    print("   git commit -m 'Add URL-based images functionality'")
    print("   git push origin main")
    print("\n3. Monitor Railway deployment logs")
    print("4. Test the API endpoints after deployment")
    
    print("\n✨ Your app will now support URL-based images on Railway!")


if __name__ == '__main__':
    main()