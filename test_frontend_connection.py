#!/usr/bin/env python3
"""
Test Frontend-Backend Connection
Test CORS and API connectivity between frontend domains and Railway backend
"""

import requests
import json


def test_cors_preflight(backend_url, frontend_origin):
    """Test CORS preflight request"""
    print(f"Testing CORS preflight from {frontend_origin}...")
    
    headers = {
        'Origin': frontend_origin,
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Content-Type'
    }
    
    try:
        response = requests.options(f"{backend_url}/api/products/", headers=headers, timeout=10)
        
        if response.status_code == 200:
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            }
            
            print(f"  ✅ CORS preflight successful")
            print(f"     Allowed Origin: {cors_headers['Access-Control-Allow-Origin']}")
            return True
        else:
            print(f"  ❌ CORS preflight failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ CORS preflight error: {e}")
        return False


def test_api_request(backend_url, frontend_origin):
    """Test actual API request with origin header"""
    print(f"Testing API request from {frontend_origin}...")
    
    headers = {
        'Origin': frontend_origin,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f"{backend_url}/api/products/", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ API request successful")
            print(f"     Products found: {len(data)}")
            print(f"     CORS header: {response.headers.get('Access-Control-Allow-Origin', 'Not set')}")
            return True
        else:
            print(f"  ❌ API request failed: {response.status_code}")
            print(f"     Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"  ❌ API request error: {e}")
        return False


def test_backend_health(backend_url):
    """Test if backend is responding"""
    print(f"Testing backend health at {backend_url}...")
    
    try:
        response = requests.get(f"{backend_url}/api/products/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Backend is healthy")
            print(f"     Products available: {len(data)}")
            return True
        else:
            print(f"  ❌ Backend health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Backend health check error: {e}")
        return False


def main():
    """Main test function"""
    print("🔗 Frontend-Backend Connection Test")
    print("=" * 45)
    
    # Your Railway backend URL
    backend_url = "https://entstores-production.up.railway.app"
    
    # Your frontend domains
    frontend_domains = [
        "https://www.enontinoclothingstore.com",
        "https://ent-stores-git-main-bassys-projects-fca17413.vercel.app",
        "https://ent-stores-jdo7tlnez-bassys-projects-fca17413.vercel.app"
    ]
    
    print(f"Backend URL: {backend_url}")
    print(f"Testing {len(frontend_domains)} frontend domains")
    print()
    
    # Test backend health first
    if not test_backend_health(backend_url):
        print("❌ Backend is not responding. Check Railway deployment.")
        return
    
    print()
    
    # Test each frontend domain
    results = {}
    
    for domain in frontend_domains:
        print(f"🌐 Testing domain: {domain}")
        print("-" * 50)
        
        cors_ok = test_cors_preflight(backend_url, domain)
        api_ok = test_api_request(backend_url, domain)
        
        results[domain] = {
            'cors': cors_ok,
            'api': api_ok,
            'overall': cors_ok and api_ok
        }
        
        print()
    
    # Summary
    print("📊 Test Results Summary")
    print("=" * 30)
    
    for domain, result in results.items():
        status = "✅ PASS" if result['overall'] else "❌ FAIL"
        domain_short = domain.replace("https://", "").replace("www.", "")[:40]
        print(f"{status} {domain_short}")
        if not result['overall']:
            if not result['cors']:
                print(f"     - CORS preflight failed")
            if not result['api']:
                print(f"     - API request failed")
    
    # Overall result
    all_passed = all(result['overall'] for result in results.values())
    
    if all_passed:
        print(f"\n🎉 All frontend domains can connect to backend!")
        print(f"\n📋 Next Steps:")
        print(f"1. Update your frontend API base URL to: {backend_url}")
        print(f"2. Test actual frontend functionality")
        print(f"3. Check browser console for any remaining CORS issues")
    else:
        print(f"\n⚠️  Some domains failed connection tests")
        print(f"\n🔧 Troubleshooting:")
        print(f"1. Check Railway deployment logs: railway logs")
        print(f"2. Verify CORS settings in Django settings.py")
        print(f"3. Ensure all domains are in CORS_ALLOWED_ORIGINS")
        print(f"4. Check if backend is fully deployed")


if __name__ == '__main__':
    main()