#!/usr/bin/env python
"""
Test production API endpoints to diagnose frontend data issues
"""
import requests
import json

# Production API base URL
API_BASE_URL = "https://entstores-production.up.railway.app/api/shop"

def test_endpoint(url, description):
    """Test a single API endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Success - Response type: {type(data)}")
                
                if isinstance(data, dict):
                    if 'results' in data:
                        print(f"   Results count: {len(data['results'])}")
                        if data['results']:
                            print(f"   First item keys: {list(data['results'][0].keys())}")
                    elif 'count' in data:
                        print(f"   Count: {data['count']}")
                    else:
                        print(f"   Keys: {list(data.keys())}")
                elif isinstance(data, list):
                    print(f"   List length: {len(data)}")
                    if data:
                        print(f"   First item keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'Not a dict'}")
                
                return True, data
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON response")
                print(f"   Content: {response.text[:200]}...")
                return False, None
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Content: {response.text[:200]}...")
            return False, None
            
    except requests.exceptions.Timeout:
        print(f"❌ Timeout error")
        return False, None
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection error")
        return False, None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False, None

def main():
    print("🔍 Testing Production API Endpoints")
    print("=" * 60)
    
    # Test basic health check
    health_success, _ = test_endpoint("https://entstores-production.up.railway.app/api/health/", "Health Check")
    
    if not health_success:
        print("\n❌ Health check failed - API might be down")
        return
    
    # Test shop endpoints
    endpoints = [
        (f"{API_BASE_URL}/products/", "Products List"),
        (f"{API_BASE_URL}/simple-products/", "Simple Products"),
        (f"{API_BASE_URL}/debug-products/", "Debug Products"),
        (f"{API_BASE_URL}/categories/", "Categories List"),
        (f"{API_BASE_URL}/stats/", "Shop Stats"),
    ]
    
    results = {}
    
    for url, description in endpoints:
        success, data = test_endpoint(url, description)
        results[description] = {
            'success': success,
            'data': data
        }
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    for endpoint, result in results.items():
        status = "✅ Working" if result['success'] else "❌ Failed"
        print(f"{endpoint}: {status}")
    
    # Check if products are available
    products_data = results.get('Products List', {}).get('data')
    simple_products_data = results.get('Simple Products', {}).get('data')
    
    if products_data:
        if isinstance(products_data, dict) and 'results' in products_data:
            product_count = len(products_data['results'])
        elif isinstance(products_data, list):
            product_count = len(products_data)
        else:
            product_count = 0
        
        print(f"\n📦 Products available: {product_count}")
        
        if product_count == 0:
            print("⚠️  No products found in the API response")
            print("💡 This explains why the frontend is empty")
        else:
            print("✅ Products are available in the API")
    
    if simple_products_data:
        if isinstance(simple_products_data, dict) and 'results' in simple_products_data:
            simple_count = len(simple_products_data['results'])
            print(f"📦 Simple products available: {simple_count}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("=" * 60)
    
    if not results.get('Products List', {}).get('success'):
        print("1. Check if the products API endpoint is working")
        print("2. Verify database has products with is_active=True")
        print("3. Check for any serialization errors in the backend")
    
    if results.get('Simple Products', {}).get('success'):
        print("1. Consider using the simple-products endpoint temporarily")
        print("2. Update frontend API service to use /simple-products/")
    
    print("\n🔧 Next steps:")
    print("1. Check the backend logs for any errors")
    print("2. Verify products exist in the admin panel")
    print("3. Test the API endpoints manually")

if __name__ == '__main__':
    main()