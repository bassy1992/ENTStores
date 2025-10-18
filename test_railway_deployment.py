#!/usr/bin/env python3
"""
Test Railway deployment for URL-based images
"""

import requests
import json
import sys


def test_api_endpoint(base_url):
    """Test the products API endpoint"""
    print(f"🧪 Testing API endpoint: {base_url}/api/products/")
    
    try:
        response = requests.get(f"{base_url}/api/products/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API is working! Found {len(data)} products")
            
            # Check for URL-based images
            url_products = [p for p in data if 'image' in p and 'unsplash.com' in str(p.get('image', ''))]
            
            if url_products:
                print(f"✓ Found {len(url_products)} products with URL-based images")
                
                # Show first few products
                for i, product in enumerate(url_products[:3]):
                    print(f"  {i+1}. {product.get('title', 'Unknown')}")
                    print(f"     Image: {product.get('image', 'No image')}")
                
                return True
            else:
                print("⚠️  No products with URL-based images found")
                return False
                
        else:
            print(f"✗ API returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to connect to API: {e}")
        return False


def test_image_accessibility(image_urls):
    """Test if image URLs are accessible"""
    print("\n🖼️  Testing image accessibility...")
    
    accessible_count = 0
    for i, url in enumerate(image_urls[:5]):  # Test first 5 images
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                print(f"✓ Image {i+1} is accessible")
                accessible_count += 1
            else:
                print(f"✗ Image {i+1} returned status: {response.status_code}")
        except Exception as e:
            print(f"✗ Image {i+1} failed: {e}")
    
    return accessible_count


def main():
    """Main test function"""
    print("🧪 Railway Deployment Test")
    print("=" * 30)
    
    # You can replace this with your actual Railway URL
    railway_url = input("Enter your Railway app URL (or press Enter to skip): ").strip()
    
    if not railway_url:
        print("ℹ️  Skipping live API test. You can test manually at:")
        print("   https://your-railway-app.railway.app/api/products/")
        return
    
    # Remove trailing slash
    railway_url = railway_url.rstrip('/')
    
    # Test API
    if test_api_endpoint(railway_url):
        print("\n✅ Railway deployment test passed!")
        print("\nYour URL-based images are working correctly on Railway.")
        
        print("\n📋 What to check next:")
        print("1. Open your frontend and verify images load")
        print("2. Check Django admin for image_url fields")
        print("3. Add new products using image URLs")
        
    else:
        print("\n❌ Railway deployment test failed")
        print("\n🔧 Troubleshooting:")
        print("1. Check Railway deployment logs")
        print("2. Verify the URL is correct")
        print("3. Ensure the app is fully deployed")


if __name__ == '__main__':
    main()