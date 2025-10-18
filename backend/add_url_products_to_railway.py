#!/usr/bin/env python3
"""
Add URL-based products to Railway database
"""

import os
import sys
import django

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, Category


def add_sample_url_products():
    """Add sample products with URL-based images"""
    print("Adding sample products with URL-based images to Railway...")
    
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
        },
        {
            "id": "ent-jacket-001",
            "title": "ENT Winter Jacket",
            "price": "89.99",
            "description": "Warm and stylish winter jacket with ENT branding. Perfect for cold weather.",
            "image_url": "https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400&h=400&fit=crop&crop=center",
            "category": "jackets",
            "stock_quantity": 15,
            "is_featured": True
        },
        {
            "id": "ent-shorts-001",
            "title": "ENT Summer Shorts",
            "price": "29.99",
            "description": "Comfortable shorts for summer activities. Lightweight and breathable fabric.",
            "image_url": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&h=400&fit=crop&crop=center",
            "category": "shorts",
            "stock_quantity": 40,
            "is_featured": False
        },
        {
            "id": "ent-cap-001",
            "title": "ENT Baseball Cap",
            "price": "19.99",
            "description": "Classic baseball cap with ENT logo. Adjustable fit for maximum comfort.",
            "image_url": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=400&fit=crop&crop=center",
            "category": "headwear",
            "stock_quantity": 60,
            "is_featured": False
        },
        {
            "id": "ent-tracksuit-001",
            "title": "ENT Complete Tracksuit",
            "price": "79.99",
            "description": "Complete tracksuit set including jacket and pants. Perfect for sports and casual wear.",
            "image_url": "https://images.unsplash.com/photo-1506629905607-d9f02a6a0e7b?w=400&h=400&fit=crop&crop=center",
            "category": "tracksuits",
            "stock_quantity": 20,
            "is_featured": True
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
            print(f"✓ {action} product: {product.title}")
            success_count += 1
            
        except Category.DoesNotExist:
            print(f"✗ Category '{product_data['category']}' not found for product {product_data['id']}")
        except Exception as e:
            print(f"✗ Error adding product {product_data['id']}: {e}")
    
    print(f"\nSuccessfully processed {success_count} out of {len(sample_products)} products")
    return success_count


def test_url_images():
    """Test that URL images are working"""
    print("\nTesting URL-based images...")
    
    # Get products with image URLs
    products_with_urls = Product.objects.filter(image_url__isnull=False).exclude(image_url='')
    
    if not products_with_urls:
        print("✗ No products with image URLs found")
        return False
    
    print(f"Found {products_with_urls.count()} products with URL-based images:")
    
    for product in products_with_urls[:3]:  # Test first 3
        image_url = product.get_image_url()
        print(f"  - {product.title}: {image_url}")
    
    return True


def main():
    """Main function"""
    print("Railway URL-Based Images Setup")
    print("=" * 35)
    
    try:
        # Add sample products
        success_count = add_sample_url_products()
        
        if success_count > 0:
            # Test the functionality
            if test_url_images():
                print("\n✓ URL-based images are working correctly!")
                print("\nNext steps:")
                print("1. Check your API: /api/products/")
                print("2. Verify images load in your frontend")
                print("3. Add more products using image URLs")
            else:
                print("\n✗ URL-based images test failed")
        else:
            print("\n✗ No products were added successfully")
            
    except Exception as e:
        print(f"\n✗ Error during setup: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()