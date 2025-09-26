#!/usr/bin/env python3
"""
Fix script to update stock validation and check current stock status
"""

import os
import sys
import django

# Setup Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, ProductVariant

def check_and_fix_stock():
    """Check current stock status and fix any issues"""
    print("🔍 Checking Stock Status")
    print("=" * 50)
    
    # Check all products
    products = Product.objects.all()
    print(f"\n📦 Found {products.count()} products")
    
    out_of_stock_products = []
    low_stock_products = []
    
    for product in products:
        print(f"\n🏷️  {product.title} (ID: {product.id})")
        print(f"   📊 Stock: {product.stock_quantity}")
        print(f"   ✅ Active: {product.is_active}")
        print(f"   🔄 In Stock (calculated): {product.is_in_stock}")
        
        # Check if product has variants
        variants = product.variants.all() if hasattr(product, 'variants') else []
        if variants.exists():
            print(f"   🎨 Variants: {variants.count()}")
            total_variant_stock = sum(v.stock_quantity for v in variants if v.is_available)
            print(f"   📦 Total variant stock: {total_variant_stock}")
            
            for variant in variants:
                print(f"      - {variant.size.name if variant.size else 'No Size'} / "
                      f"{variant.color.name if variant.color else 'No Color'}: "
                      f"{variant.stock_quantity} (Available: {variant.is_available})")
        
        # Categorize products
        if not product.is_in_stock:
            out_of_stock_products.append(product)
        elif product.stock_quantity <= 5:
            low_stock_products.append(product)
    
    # Summary
    print(f"\n📋 STOCK SUMMARY")
    print("=" * 30)
    print(f"🔴 Out of stock: {len(out_of_stock_products)} products")
    for product in out_of_stock_products:
        print(f"   - {product.title} (Stock: {product.stock_quantity})")
    
    print(f"\n🟡 Low stock (≤5): {len(low_stock_products)} products")
    for product in low_stock_products:
        print(f"   - {product.title} (Stock: {product.stock_quantity})")
    
    # Check for products that might be incorrectly showing as in stock
    print(f"\n🔍 POTENTIAL ISSUES")
    print("=" * 30)
    
    issues_found = False
    for product in products:
        # Check if product shows as in stock but has 0 stock
        if product.stock_quantity == 0:
            variants_with_stock = []
            if hasattr(product, 'variants'):
                variants_with_stock = product.variants.filter(
                    stock_quantity__gt=0, 
                    is_available=True
                )
            
            if not variants_with_stock.exists() and product.is_in_stock:
                print(f"⚠️  {product.title}: Shows in stock but has 0 stock and no available variants")
                issues_found = True
    
    if not issues_found:
        print("✅ No stock calculation issues found")
    
    print(f"\n🛠️  RECOMMENDATIONS")
    print("=" * 30)
    print("1. Deploy the updated backend with stock validation")
    print("2. Test the stock validation endpoint")
    print("3. Update frontend to use stock validation before checkout")
    print("4. Monitor stock levels regularly")
    
    if out_of_stock_products:
        print(f"\n⚠️  IMMEDIATE ACTION NEEDED:")
        print(f"   {len(out_of_stock_products)} products are out of stock")
        print("   Users should not be able to purchase these items")

if __name__ == "__main__":
    check_and_fix_stock()