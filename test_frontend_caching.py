#!/usr/bin/env python
import requests
import time
import json

def test_caching_issues():
    """Test for potential caching issues affecting frontend display"""
    
    print("🔍 Testing for caching issues with product: fghfhghgh")
    print("=" * 60)
    
    # Test 1: Direct API call
    print("\n1️⃣ Direct API Test (no cache busting):")
    test_api_direct()
    
    # Test 2: Cache busting with timestamp
    print("\n2️⃣ Cache Busting Test (with timestamp):")
    test_api_cache_busting()
    
    # Test 3: Multiple calls to check consistency
    print("\n3️⃣ Consistency Test (multiple calls):")
    test_api_consistency()
    
    # Test 4: Different endpoints
    print("\n4️⃣ Different Endpoints Test:")
    test_different_endpoints()
    
    print("\n" + "=" * 60)
    print("🔧 CACHE BUSTING SOLUTIONS:")
    print_cache_solutions()

def test_api_direct():
    """Test direct API call"""
    try:
        url = "https://entstores-production.up.railway.app/api/shop/products/fghfhghgh/"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Status: {response.status_code}")
            print(f"  📦 Title: {data.get('title')}")
            print(f"  📊 Main Stock: {data.get('stock_quantity')}")
            print(f"  ✅ Is In Stock: {data.get('is_in_stock')}")
            print(f"  🎯 Variants: {len(data.get('variants', []))}")
            
            # Check response headers for caching info
            cache_control = response.headers.get('Cache-Control', 'Not set')
            etag = response.headers.get('ETag', 'Not set')
            print(f"  🔄 Cache-Control: {cache_control}")
            print(f"  🏷️  ETag: {etag}")
        else:
            print(f"  ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def test_api_cache_busting():
    """Test API with cache busting parameters"""
    try:
        timestamp = int(time.time())
        url = f"https://entstores-production.up.railway.app/api/shop/products/fghfhghgh/?_t={timestamp}&_cb={timestamp}"
        
        response = requests.get(url, headers={
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Status: {response.status_code}")
            print(f"  📦 Title: {data.get('title')}")
            print(f"  📊 Main Stock: {data.get('stock_quantity')}")
            print(f"  ✅ Is In Stock: {data.get('is_in_stock')}")
            print(f"  🎯 Variants: {len(data.get('variants', []))}")
        else:
            print(f"  ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

def test_api_consistency():
    """Test multiple calls for consistency"""
    results = []
    
    for i in range(3):
        try:
            timestamp = int(time.time()) + i
            url = f"https://entstores-production.up.railway.app/api/shop/products/fghfhghgh/?_t={timestamp}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    'call': i + 1,
                    'is_in_stock': data.get('is_in_stock'),
                    'stock_quantity': data.get('stock_quantity'),
                    'variants_count': len(data.get('variants', []))
                }
                results.append(result)
                print(f"  Call {i+1}: is_in_stock={result['is_in_stock']}, stock={result['stock_quantity']}, variants={result['variants_count']}")
            else:
                print(f"  Call {i+1}: Error {response.status_code}")
                
            time.sleep(1)  # Wait 1 second between calls
        except Exception as e:
            print(f"  Call {i+1}: Error - {e}")
    
    # Check consistency
    if len(results) > 1:
        first_result = results[0]
        consistent = all(
            r['is_in_stock'] == first_result['is_in_stock'] and
            r['stock_quantity'] == first_result['stock_quantity']
            for r in results
        )
        print(f"  🔄 Consistency: {'✅ Consistent' if consistent else '❌ Inconsistent'}")

def test_different_endpoints():
    """Test different API endpoints"""
    endpoints = [
        ("Product Detail", "https://entstores-production.up.railway.app/api/shop/products/fghfhghgh/"),
        ("Products List", "https://entstores-production.up.railway.app/api/shop/products/"),
    ]
    
    for name, base_url in endpoints:
        try:
            timestamp = int(time.time())
            url = f"{base_url}?_t={timestamp}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                if name == "Product Detail":
                    is_in_stock = data.get('is_in_stock')
                    stock_qty = data.get('stock_quantity')
                else:  # Products List
                    results = data.get('results', [])
                    target_product = next((p for p in results if p.get('slug') == 'fghfhghgh'), None)
                    if target_product:
                        is_in_stock = target_product.get('is_in_stock')
                        stock_qty = target_product.get('stock_quantity')
                    else:
                        is_in_stock = None
                        stock_qty = None
                
                print(f"  {name}: is_in_stock={is_in_stock}, stock={stock_qty}")
            else:
                print(f"  {name}: Error {response.status_code}")
        except Exception as e:
            print(f"  {name}: Error - {e}")

def print_cache_solutions():
    """Print solutions for cache issues"""
    print("""
🔧 FRONTEND CACHE BUSTING SOLUTIONS:

1. **API Service Cache Busting** (Recommended):
   Add timestamp to API calls in frontend/services/api.ts:
   
   ```typescript
   const timestamp = Date.now();
   const response = await fetch(`${API_BASE_URL}/products/${slug}/?_t=${timestamp}`);
   ```

2. **Browser Hard Refresh**:
   - Press Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
   - Or open DevTools → Network → check "Disable cache"

3. **CDN Cache Purge**:
   - If using Cloudflare/similar: Purge cache for API endpoints
   - Or add cache-control headers to API responses

4. **Frontend State Management**:
   - Clear React state/context when navigating
   - Force re-fetch on component mount

5. **API Response Headers** (Backend fix):
   Add to Django views:
   ```python
   response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
   response['Pragma'] = 'no-cache'
   response['Expires'] = '0'
   ```

🎯 IMMEDIATE TEST:
Visit: https://www.enontinoclothingstore.com/product/fghfhghgh
1. Open DevTools → Network tab
2. Check "Disable cache"
3. Refresh the page
4. Check if stock status is now correct
""")

if __name__ == "__main__":
    test_caching_issues()