#!/usr/bin/env python3
"""
Test CORS configuration after the fix
"""

import requests
import json

def test_cors_configuration():
    """Test CORS configuration on the backend"""
    print("🧪 Testing CORS Configuration Fix")
    print("=" * 50)
    
    backend_url = "https://entstores.onrender.com"
    frontend_origin = "https://www.enontinoclothingstore.com"
    
    # Test 1: CORS test endpoint
    print("\n1️⃣ Testing CORS configuration endpoint...")
    try:
        response = requests.get(f"{backend_url}/api/cors-test/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ CORS test endpoint accessible")
            print(f"   🌐 CORS allow all origins: {data.get('cors_allow_all_origins')}")
            print(f"   📋 CORS allowed origins: {len(data.get('cors_allowed_origins', []))} origins")
            print(f"   🔧 CORS middleware installed: {data.get('cors_middleware_installed')}")
            print(f"   📦 corsheaders installed: {data.get('corsheaders_installed')}")
        else:
            print(f"   ❌ CORS test endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing CORS endpoint: {e}")
    
    # Test 2: Categories API with Origin header
    print(f"\n2️⃣ Testing categories API with Origin header...")
    try:
        headers = {
            'Origin': frontend_origin,
            'User-Agent': 'Mozilla/5.0 (Test)',
        }
        response = requests.get(f"{backend_url}/api/shop/categories/", headers=headers)
        print(f"   📊 Status Code: {response.status_code}")
        print(f"   🔗 Origin Header: {frontend_origin}")
        
        # Check CORS headers in response
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        print(f"   📋 CORS Response Headers:")
        for header, value in cors_headers.items():
            if value:
                print(f"      {header}: {value}")
            else:
                print(f"      {header}: ❌ Not present")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Categories API accessible")
            print(f"   📦 Categories returned: {len(data.get('results', []))}")
        else:
            print(f"   ❌ Categories API failed: {response.status_code}")
            print(f"   📄 Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Error testing categories API: {e}")
    
    # Test 3: Preflight OPTIONS request
    print(f"\n3️⃣ Testing preflight OPTIONS request...")
    try:
        headers = {
            'Origin': frontend_origin,
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'content-type',
        }
        response = requests.options(f"{backend_url}/api/shop/categories/", headers=headers)
        print(f"   📊 OPTIONS Status Code: {response.status_code}")
        
        # Check preflight response headers
        preflight_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Max-Age': response.headers.get('Access-Control-Max-Age'),
        }
        
        print(f"   📋 Preflight Response Headers:")
        for header, value in preflight_headers.items():
            if value:
                print(f"      {header}: {value}")
            else:
                print(f"      {header}: ❌ Not present")
                
        if response.status_code in [200, 204]:
            print(f"   ✅ Preflight request successful")
        else:
            print(f"   ❌ Preflight request failed")
            
    except Exception as e:
        print(f"   ❌ Error testing preflight request: {e}")
    
    # Test 4: Health check
    print(f"\n4️⃣ Testing health check endpoint...")
    try:
        response = requests.get(f"{backend_url}/api/health/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check: {data.get('status')}")
            print(f"   🌐 CORS enabled: {data.get('cors_enabled')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing health check: {e}")
    
    print(f"\n📋 Summary:")
    print(f"   - Backend URL: {backend_url}")
    print(f"   - Frontend Origin: {frontend_origin}")
    print(f"   - CORS should now be configured to allow all origins in production")
    print(f"   - If issues persist, check Render deployment logs")

def test_from_browser():
    """Instructions for testing from browser"""
    print(f"\n🌐 Browser Testing Instructions:")
    print(f"=" * 30)
    print(f"1. Open browser developer tools (F12)")
    print(f"2. Go to Console tab")
    print(f"3. Run this JavaScript:")
    print(f"""
fetch('https://entstores.onrender.com/api/shop/categories/')
  .then(response => response.json())
  .then(data => console.log('✅ CORS working:', data))
  .catch(error => console.error('❌ CORS error:', error));
""")
    print(f"4. If successful, you should see categories data")
    print(f"5. If failed, check for CORS error in console")

if __name__ == "__main__":
    test_cors_configuration()
    test_from_browser()