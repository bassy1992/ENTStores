#!/usr/bin/env python3
"""
Create a test scenario where a product is truly out of stock
"""

import requests
import json

def test_truly_out_of_stock():
    """Test what happens when a product and all its variants are out of stock"""
    print("🧪 Testing Truly Out of Stock Scenario")
    print("=" * 50)
    
    # For testing purposes, let's simulate what the frontend should do
    # when encountering a product that's truly out of stock
    
    # Simulate a product with no stock
    mock_product = {
        'id': 'TEST_PRODUCT',
        'title': 'Test Out of Stock Product',
        'stock_quantity': 0,
        'is_in_stock': False,  # This would be False if no variants have stock
        'variants': [
            {
                'id': 1,
                'size': {'display_name': 'Small'},
                'color': {'name': 'Red'},
                'stock_quantity': 0,
                'is_available': True,
                'is_in_stock': False
            },
            {
                'id': 2,
                'size': {'display_name': 'Medium'},
                'color': {'name': 'Blue'},
                'stock_quantity': 0,
                'is_available': True,
                'is_in_stock': False
            }
        ]
    }
    
    print("📦 Mock Product:")
    print(f"   Title: {mock_product['title']}")
    print(f"   Main Stock: {mock_product['stock_quantity']}")
    print(f"   Is In Stock: {mock_product['is_in_stock']}")
    print(f"   Variants: {len(mock_product['variants'])}")
    
    for variant in mock_product['variants']:
        size = variant['size']['display_name']
        color = variant['color']['name']
        stock = variant['stock_quantity']
        in_stock = variant['is_in_stock']
        print(f"     - {size} {color}: {stock} units, in_stock: {in_stock}")
    
    print(f"\n🎭 Frontend Behavior Analysis:")
    
    # Check ProductCard logic
    is_out_of_stock_card = mock_product['is_in_stock'] == False or mock_product['stock_quantity'] == 0
    print(f"   ProductCard isOutOfStock: {is_out_of_stock_card}")
    
    if is_out_of_stock_card:
        print(f"   ✅ ProductCard should show 'Out of Stock' badge")
        print(f"   ✅ ProductCard should hide 'Add' button")
        print(f"   ✅ ProductCard should gray out image")
    else:
        print(f"   ❌ ProductCard would show as available")
    
    # Check ProductDetails logic
    print(f"\n   ProductDetails behavior:")
    has_in_stock_variants = any(v['is_in_stock'] for v in mock_product['variants'])
    print(f"   Has in-stock variants: {has_in_stock_variants}")
    
    if not has_in_stock_variants:
        print(f"   ✅ All variant selections should show 'Out of Stock'")
        print(f"   ✅ Add to Cart button should be disabled")
    else:
        print(f"   ❌ Some variants would be available")
    
    # Check cart context logic
    print(f"\n   Cart Context validation:")
    print(f"   is_in_stock check: {mock_product['is_in_stock']}")
    print(f"   stock_quantity check: {mock_product['stock_quantity']}")
    
    if not mock_product['is_in_stock'] or mock_product['stock_quantity'] == 0:
        print(f"   ✅ Cart.add() should reject with warning")
    else:
        print(f"   ❌ Cart.add() would allow adding")
    
    print(f"\n📋 Summary for Truly Out of Stock Product:")
    print(f"   - ProductCard: {'✅ Correctly blocked' if is_out_of_stock_card else '❌ Would show as available'}")
    print(f"   - ProductDetails: {'✅ Correctly blocked' if not has_in_stock_variants else '❌ Would allow variants'}")
    print(f"   - Cart Context: {'✅ Correctly blocked' if not mock_product['is_in_stock'] else '❌ Would allow adding'}")

def test_current_products_behavior():
    """Test how current products should behave"""
    print(f"\n🔍 Current Products Analysis")
    print("=" * 30)
    
    # Test the fghfhghgh product behavior
    product_data = {
        'id': '67',
        'title': 'fghfhghgh',
        'stock_quantity': 0,
        'is_in_stock': True,  # True because variants have stock
        'variants': [
            {'stock_quantity': 89, 'is_in_stock': True},
            {'stock_quantity': 98, 'is_in_stock': True}
        ]
    }
    
    print(f"📦 Product: {product_data['title']}")
    
    # ProductCard logic
    is_out_of_stock_card = product_data['is_in_stock'] == False or product_data['stock_quantity'] == 0
    print(f"   ProductCard isOutOfStock: {is_out_of_stock_card}")
    
    # This is the issue! The product has stock_quantity=0 but is_in_stock=True
    # So isOutOfStock = False OR True = True (should show as out of stock in card)
    # But is_in_stock=True (so product is actually available via variants)
    
    print(f"\n🎯 The Issue:")
    print(f"   - ProductCard sees stock_quantity=0, so shows 'Out of Stock'")
    print(f"   - But ProductDetails allows selecting variants with stock")
    print(f"   - This creates inconsistent UX!")
    
    print(f"\n💡 Solution:")
    print(f"   - ProductCard should check if ANY variants have stock")
    print(f"   - If variants exist and have stock, show 'Select Options' instead of 'Add'")
    print(f"   - Only show 'Out of Stock' if NO variants have stock")

if __name__ == "__main__":
    test_truly_out_of_stock()
    test_current_products_behavior()