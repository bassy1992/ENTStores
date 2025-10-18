#!/usr/bin/env python3
"""
Fix Railway Media Storage Issue
Railway doesn't have persistent storage, so we need to use cloud storage
"""
import os
import requests
import json

def check_github_repo():
    """Check if GitHub media repository exists"""
    repo_owner = "bassy1992"
    repo_name = "ENTstore-media"
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("✅ GitHub media repository exists")
        return True
    else:
        print("❌ GitHub media repository not found")
        print(f"Create it at: https://github.com/new")
        print(f"Repository name: {repo_name}")
        return False

def test_railway_api():
    """Test if Railway backend is accessible"""
    try:
        response = requests.get("https://entstores-production.up.railway.app/api/shop/products/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Railway API accessible - Found {len(data.get('results', []))} products")
            
            # Check for products with media
            products_with_media = []
            for product in data.get('results', []):
                if product.get('image_url'):
                    products_with_media.append({
                        'name': product.get('name'),
                        'image_url': product.get('image_url')
                    })
            
            print(f"📸 Products with images: {len(products_with_media)}")
            return products_with_media
        else:
            print(f"❌ Railway API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Railway API connection failed: {e}")
        return []

def check_media_urls(products):
    """Check which media URLs are working"""
    working_urls = []
    broken_urls = []
    
    for product in products[:5]:  # Check first 5 products
        image_url = product['image_url']
        try:
            response = requests.head(image_url, timeout=5)
            if response.status_code == 200:
                working_urls.append(image_url)
                print(f"✅ {product['name']}: {image_url}")
            else:
                broken_urls.append(image_url)
                print(f"❌ {product['name']}: {image_url} (Status: {response.status_code})")
        except Exception as e:
            broken_urls.append(image_url)
            print(f"❌ {product['name']}: {image_url} (Error: {e})")
    
    return working_urls, broken_urls

def main():
    print("🔧 Railway Media Storage Diagnostic")
    print("=" * 50)
    
    # Check GitHub repository
    print("\n1️⃣ Checking GitHub media repository...")
    github_ok = check_github_repo()
    
    # Test Railway API
    print("\n2️⃣ Testing Railway API...")
    products = test_railway_api()
    
    if products:
        print("\n3️⃣ Checking media URLs...")
        working, broken = check_media_urls(products)
        
        print(f"\n📊 Results:")
        print(f"✅ Working URLs: {len(working)}")
        print(f"❌ Broken URLs: {len(broken)}")
        
        if broken:
            print(f"\n💡 Solutions:")
            print(f"1. Set up GitHub token in Railway environment variables:")
            print(f"   railway variables set GITHUB_TOKEN='your_github_token'")
            print(f"2. Create GitHub repository: ENTstore-media")
            print(f"3. Re-upload images through Django admin")
            print(f"4. Or use Cloudinary for automatic cloud storage")
    
    print(f"\n🔗 Useful links:")
    print(f"- Railway Dashboard: https://railway.app/dashboard")
    print(f"- Django Admin: https://entstores-production.up.railway.app/admin/")
    print(f"- GitHub Token: https://github.com/settings/tokens")

if __name__ == "__main__":
    main()