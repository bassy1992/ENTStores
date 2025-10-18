#!/usr/bin/env python
import requests
import json

def test_out_of_stock_scenarios():
    """Test different out of stock scenarios"""
    
    print("🧪 Testing out of stock display scenarios...")
    
    # Test the coral pink shorts (should be IN stock due to variants)
    print("\n1️⃣ Testing SHORTS Coral Pink (has variants with stock):")
    test_product_stock("shorts-coral-pink")
    
    # Get list of all products to find one that's actually out of stock
    print("\n2️⃣ Finding products that are actually out of stock:")
    try:
        response = requests.get("https://entstores-production.up.railway.app/api/shop/products/")
        if response.status_code == 200:
            data = response.json()
            products = data.get('results', [])
            
            out_of_stock_products = []
            in_stock_products = []
            
            for product in products:
                if not product.get('is_in_stock', True):
                    out_of_stock_products.append(product)
                else:
                    in_stock_products.append(product)
            
            print(f"📊 Found {len(out_of_stock_products)} out of stock products")
            print(f"📊 Found {len(in_stock_products)} in stock products")
            
            # Test a few out of stock products
            for i, product in enumerate(out_of_stock_products[:3]):
                print(f"\n{i+3}️⃣ Testing {product.get('title')} (should be OUT of stock):")
                test_product_stock(product.get('slug'))
                
        else:
            print(f"❌ Error getting products list: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_product_stock(slug):
    """Test a specific product's stock status"""
    try:
        # Test product detail API
        detail_url = f"https://entstores-production.up.railway.app/api/shop/products/{slug}/"
        response = requests.get(detail_url)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"  📦 Product: {data.get('title', 'N/A')}")
            print(f"  📊 Main Stock: {data.get('stock_quantity', 'N/A')}")
            print(f"  ✅ Is In Stock: {data.get('is_in_stock', 'N/A')}")
            
            # Check variants
            variants = data.get('variants', [])
            if variants:
                print(f"  🎯 Variants: {len(variants)}")
                total_variant_stock = 0
                in_stock_variants = 0
                
                for variant in variants:
                    stock = variant.get('stock_quantity', 0)
                    is_in_stock = variant.get('is_in_stock', False)
                    size = variant.get('size', {}).get('name', 'N/A')
                    color = variant.get('color', {}).get('name', 'N/A')
                    
                    total_variant_stock += stock
                    if is_in_stock:
                        in_stock_variants += 1
                    
                    print(f"    - {size} {color}: {stock} units, in_stock: {is_in_stock}")
                
                print(f"  📈 Total variant stock: {total_variant_stock}")
                print(f"  ✅ In-stock variants: {in_stock_variants}/{len(variants)}")
            else:
                print(f"  🎯 No variants")
            
            # Determine expected frontend behavior
            if data.get('is_in_stock'):
                if variants:
                    print(f"  🎭 Frontend should: Show variant stock badges, allow adding to cart when variant selected")
                else:
                    print(f"  🎭 Frontend should: Show 'In Stock ({data.get('stock_quantity')})', allow adding to cart")
            else:
                print(f"  🎭 Frontend should: Show 'Out of Stock' badge, disable add to cart button")
                
        elif response.status_code == 404:
            print(f"  ❌ Product not found: {slug}")
        else:
            print(f"  ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    test_out_of_stock_scenarios()