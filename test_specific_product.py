#!/usr/bin/env python
import requests
import json

def test_fghfhghgh_product():
    """Test the specific product that's allowing add to cart when out of stock"""
    
    print("🔍 Testing product: fghfhghgh")
    print("URL: https://www.enontinoclothingstore.com/product/fghfhghgh")
    
    # Test product detail API
    detail_url = "https://entstores-production.up.railway.app/api/shop/products/fghfhghgh/"
    
    try:
        response = requests.get(detail_url)
        print(f"API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n📦 Product Details:")
            print(f"  Title: {data.get('title', 'N/A')}")
            print(f"  Main Stock: {data.get('stock_quantity', 'N/A')}")
            print(f"  Is In Stock: {data.get('is_in_stock', 'N/A')}")
            print(f"  Is Active: {data.get('is_active', 'N/A')}")
            
            # Check variants
            variants = data.get('variants', [])
            print(f"\n🎯 Variants Analysis:")
            print(f"  Total variants: {len(variants)}")
            
            if variants:
                total_variant_stock = 0
                available_variants = 0
                in_stock_variants = 0
                
                for i, variant in enumerate(variants):
                    size = variant.get('size', {}).get('name', 'N/A')
                    color = variant.get('color', {}).get('name', 'N/A')
                    stock = variant.get('stock_quantity', 0)
                    is_available = variant.get('is_available', False)
                    is_in_stock = variant.get('is_in_stock', False)
                    
                    total_variant_stock += stock
                    if is_available:
                        available_variants += 1
                    if is_in_stock:
                        in_stock_variants += 1
                    
                    print(f"    {i+1}. {size} {color}:")
                    print(f"       Stock: {stock}")
                    print(f"       Available: {is_available}")
                    print(f"       In Stock: {is_in_stock}")
                
                print(f"\n📊 Summary:")
                print(f"  Total variant stock: {total_variant_stock}")
                print(f"  Available variants: {available_variants}/{len(variants)}")
                print(f"  In-stock variants: {in_stock_variants}/{len(variants)}")
                
                # Determine what frontend should show
                print(f"\n🎭 Frontend Behavior:")
                if data.get('is_in_stock'):
                    print(f"  ✅ Product shows as 'In Stock' (correct if variants have stock)")
                    if in_stock_variants > 0:
                        print(f"  ✅ Should allow adding to cart when variant selected")
                        print(f"  ⚠️  ISSUE: If showing as out of stock but allowing add to cart, there's a frontend bug")
                    else:
                        print(f"  ❌ BACKEND BUG: Product shows in stock but no variants have stock")
                else:
                    print(f"  ❌ Product shows as 'Out of Stock'")
                    print(f"  ❌ Should NOT allow adding to cart")
            else:
                print(f"  No variants found")
                if data.get('is_in_stock'):
                    print(f"  ✅ Should allow adding to cart (main stock: {data.get('stock_quantity')})")
                else:
                    print(f"  ❌ Should NOT allow adding to cart (no stock)")
            
            # Test what the shop page API returns
            print(f"\n🛍️  Shop Page API Test:")
            test_shop_page_for_product("fghfhghgh")
            
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_shop_page_for_product(slug):
    """Test how the product appears in shop page API"""
    try:
        response = requests.get("https://entstores-production.up.railway.app/api/shop/products/")
        if response.status_code == 200:
            data = response.json()
            products = data.get('results', [])
            
            target_product = None
            for product in products:
                if product.get('slug') == slug:
                    target_product = product
                    break
            
            if target_product:
                print(f"  Found in shop page:")
                print(f"    Title: {target_product.get('title')}")
                print(f"    Stock: {target_product.get('stock_quantity')}")
                print(f"    In Stock: {target_product.get('is_in_stock')}")
                
                if target_product.get('is_in_stock'):
                    print(f"    🎭 Shop page: Shows as available, allows add to cart")
                else:
                    print(f"    🎭 Shop page: Shows as out of stock, disables add to cart")
            else:
                print(f"  ❌ Product not found in shop page results")
        else:
            print(f"  ❌ Shop page API error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Shop page test error: {e}")

if __name__ == "__main__":
    test_fghfhghgh_product()