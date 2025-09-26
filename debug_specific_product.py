#!/usr/bin/env python3
"""
Debug a specific product to understand its stock status
"""

import requests
import json

def debug_product(slug):
    """Debug a specific product's stock and variants"""
    print(f"🔍 Debugging product: {slug}")
    print("=" * 50)
    
    try:
        # Get product details
        response = requests.get(f"https://entstores.onrender.com/api/shop/products/{slug}/")
        if response.status_code == 200:
            product = response.json()
            
            print(f"📦 Product: {product.get('title')}")
            print(f"🆔 ID: {product.get('id')}")
            print(f"📊 Main Stock: {product.get('stock_quantity')}")
            print(f"✅ Is In Stock: {product.get('is_in_stock')}")
            print(f"🏷️  Category: {product.get('category_label')}")
            
            # Check variants
            variants = product.get('variants', [])
            print(f"\n🎯 Variants ({len(variants)}):")
            
            if variants:
                for i, variant in enumerate(variants):
                    size = variant.get('size', {})
                    color = variant.get('color', {})
                    stock = variant.get('stock_quantity', 0)
                    is_available = variant.get('is_available', False)
                    is_in_stock = variant.get('is_in_stock', False)
                    
                    print(f"  {i+1}. {size.get('display_name', 'N/A')} - {color.get('name', 'N/A')}")
                    print(f"     Stock: {stock}, Available: {is_available}, In Stock: {is_in_stock}")
                    
                    # This variant should be addable to cart if it has stock
                    if is_in_stock and stock > 0:
                        print(f"     ✅ This variant CAN be added to cart")
                    else:
                        print(f"     ❌ This variant CANNOT be added to cart")
            else:
                print("  No variants found")
            
            # Test stock validation for main product
            print(f"\n🧪 Testing stock validation for main product:")
            test_items = [{
                'product_id': product.get('id'),
                'quantity': 1
            }]
            
            validation_response = requests.post(
                "https://entstores.onrender.com/api/shop/validate-stock/", 
                json={'items': test_items}
            )
            
            if validation_response.status_code == 200:
                validation = validation_response.json()
                print(f"   Valid: {validation.get('valid')}")
                if validation.get('errors'):
                    for error in validation.get('errors'):
                        print(f"   Error: {error.get('error')}")
            
            # Test stock validation for each variant
            if variants:
                print(f"\n🧪 Testing stock validation for variants:")
                for i, variant in enumerate(variants):
                    if variant.get('is_in_stock'):
                        test_items = [{
                            'product_id': product.get('id'),
                            'quantity': 1,
                            'variant_id': variant.get('id')
                        }]
                        
                        validation_response = requests.post(
                            "https://entstores.onrender.com/api/shop/validate-stock/", 
                            json={'items': test_items}
                        )
                        
                        if validation_response.status_code == 200:
                            validation = validation_response.json()
                            size_name = variant.get('size', {}).get('display_name', 'N/A')
                            color_name = variant.get('color', {}).get('name', 'N/A')
                            print(f"   Variant {size_name}-{color_name}: Valid={validation.get('valid')}")
                            if validation.get('errors'):
                                for error in validation.get('errors'):
                                    print(f"     Error: {error.get('error')}")
            
            print(f"\n📋 Summary:")
            print(f"   - Main product stock: {product.get('stock_quantity')}")
            print(f"   - Product shows as in stock: {product.get('is_in_stock')}")
            print(f"   - Has {len(variants)} variants")
            
            in_stock_variants = [v for v in variants if v.get('is_in_stock')]
            print(f"   - {len(in_stock_variants)} variants are in stock")
            
            if len(in_stock_variants) > 0:
                print(f"   ✅ Users CAN add this product to cart by selecting an in-stock variant")
            else:
                print(f"   ❌ Users CANNOT add this product to cart (no stock)")
                
        else:
            print(f"❌ Failed to fetch product: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Test the problematic product
    debug_product("fghfhghgh")
    
    print("\n" + "="*50)
    
    # Also test a shorts product
    debug_product("shorts-coral-pink")