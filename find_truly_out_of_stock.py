#!/usr/bin/env python
import requests
import json

def find_truly_out_of_stock():
    """Find products that should be truly out of stock"""
    
    print("🔍 Analyzing all products for true out of stock scenarios...")
    
    try:
        response = requests.get("https://entstores-production.up.railway.app/api/shop/products/")
        if response.status_code == 200:
            data = response.json()
            products = data.get('results', [])
            
            print(f"📊 Analyzing {len(products)} products...")
            
            categories = {}
            
            for product in products:
                title = product.get('title', 'N/A')
                slug = product.get('slug', 'N/A')
                main_stock = product.get('stock_quantity', 0)
                is_in_stock = product.get('is_in_stock', False)
                category = product.get('category', 'unknown')
                
                if category not in categories:
                    categories[category] = []
                
                categories[category].append({
                    'title': title,
                    'slug': slug,
                    'main_stock': main_stock,
                    'is_in_stock': is_in_stock
                })
            
            print(f"\n📋 Products by category:")
            for category, products_list in categories.items():
                print(f"\n🏷️  {category.upper()}:")
                for product in products_list:
                    status = "✅ IN STOCK" if product['is_in_stock'] else "❌ OUT OF STOCK"
                    print(f"  - {product['title']} (stock: {product['main_stock']}) - {status}")
            
            # Now let's get detailed info for a few products to see their variants
            print(f"\n🔬 Detailed analysis of first few products:")
            for i, product in enumerate(data.get('results', [])[:3]):
                slug = product.get('slug')
                print(f"\n{i+1}. Analyzing {product.get('title')}:")
                analyze_product_details(slug)
                
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def analyze_product_details(slug):
    """Get detailed product info including variants"""
    try:
        detail_url = f"https://entstores-production.up.railway.app/api/shop/products/{slug}/"
        response = requests.get(detail_url)
        
        if response.status_code == 200:
            data = response.json()
            
            main_stock = data.get('stock_quantity', 0)
            is_in_stock = data.get('is_in_stock', False)
            variants = data.get('variants', [])
            
            print(f"   Main stock: {main_stock}")
            print(f"   Is in stock: {is_in_stock}")
            print(f"   Variants: {len(variants)}")
            
            if variants:
                variant_stocks = []
                for variant in variants:
                    stock = variant.get('stock_quantity', 0)
                    is_available = variant.get('is_available', False)
                    is_variant_in_stock = variant.get('is_in_stock', False)
                    size = variant.get('size', {}).get('name', 'N/A')
                    color = variant.get('color', {}).get('name', 'N/A')
                    
                    variant_stocks.append(stock)
                    print(f"     - {size} {color}: {stock} units, available: {is_available}, in_stock: {is_variant_in_stock}")
                
                total_variant_stock = sum(variant_stocks)
                print(f"   Total variant stock: {total_variant_stock}")
                
                # Logic check
                should_be_in_stock = main_stock > 0 or total_variant_stock > 0
                print(f"   Should be in stock: {should_be_in_stock} (actual: {is_in_stock})")
                
                if should_be_in_stock != is_in_stock:
                    print(f"   ⚠️  MISMATCH! Expected {should_be_in_stock}, got {is_in_stock}")
            else:
                print(f"   No variants - stock based on main product only")
                should_be_in_stock = main_stock > 0
                print(f"   Should be in stock: {should_be_in_stock} (actual: {is_in_stock})")
                
        else:
            print(f"   ❌ Error getting details: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    find_truly_out_of_stock()