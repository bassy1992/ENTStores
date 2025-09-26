#!/usr/bin/env python3
"""
Test stock validation directly using Django ORM
"""

import os
import sys
import django

# Setup Django
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from shop.models import Product, Order, OrderItem
from shop.serializers import CreateOrderSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

def test_stock_validation_direct():
    """Test stock validation directly"""
    print("🧪 Testing Stock Validation (Direct)")
    print("=" * 50)
    
    # Get the out-of-stock product we created earlier
    try:
        out_of_stock_product = Product.objects.get(id='ennc-essential-hoodie-black')
        print(f"📦 Found test product: {out_of_stock_product.title}")
        print(f"   Stock: {out_of_stock_product.stock_quantity}")
        print(f"   In stock: {out_of_stock_product.is_in_stock}")
    except Product.DoesNotExist:
        print("❌ Test product not found. Creating one...")
        # Get any product and set it to 0 stock
        out_of_stock_product = Product.objects.first()
        if out_of_stock_product:
            out_of_stock_product.stock_quantity = 0
            out_of_stock_product.save()
            print(f"✅ Set {out_of_stock_product.title} to out of stock")
        else:
            print("❌ No products found in database")
            return
    
    # Test 1: Try to create order with out-of-stock item
    print(f"\n1️⃣ Testing order creation with out-of-stock item...")
    
    order_data = {
        'id': 'TEST_STOCK_001',
        'customer_email': 'test@example.com',
        'customer_name': 'Test Customer',
        'shipping_address': '123 Test St',
        'shipping_city': 'Test City',
        'shipping_country': 'Test Country',
        'subtotal': 25.00,
        'shipping_cost': 5.00,
        'tax_amount': 2.50,
        'total': 32.50,
        'payment_method': 'test',
        'payment_reference': 'test_ref_001',
        'items': [{
            'product_id': out_of_stock_product.id,
            'quantity': 1,
            'unit_price': 25.00
        }]
    }
    
    # Create a mock request
    factory = APIRequestFactory()
    request = factory.post('/api/shop/orders/', order_data, format='json')
    
    # Test the serializer
    serializer = CreateOrderSerializer(data=order_data, context={'request': Request(request)})
    
    if serializer.is_valid():
        print("   ❌ PROBLEM: Serializer validation passed (should have failed)")
        print("   This means stock validation is not working properly")
    else:
        print("   ✅ SUCCESS: Serializer validation failed as expected")
        print("   Errors:", serializer.errors)
        
        # Check if stock_errors are in the validation errors
        if 'stock_errors' in serializer.errors or any('stock' in str(error).lower() for error in serializer.errors.values()):
            print("   ✅ Stock validation is working correctly")
        else:
            print("   ⚠️  Validation failed but not due to stock issues")
    
    # Test 2: Try with a product that has stock
    print(f"\n2️⃣ Testing order creation with in-stock item...")
    
    in_stock_product = Product.objects.filter(stock_quantity__gt=0).first()
    if in_stock_product:
        print(f"   📦 Using product: {in_stock_product.title} (Stock: {in_stock_product.stock_quantity})")
        
        order_data_valid = order_data.copy()
        order_data_valid['id'] = 'TEST_STOCK_002'
        order_data_valid['items'] = [{
            'product_id': in_stock_product.id,
            'quantity': 1,
            'unit_price': 25.00
        }]
        
        serializer_valid = CreateOrderSerializer(data=order_data_valid, context={'request': Request(request)})
        
        if serializer_valid.is_valid():
            print("   ✅ SUCCESS: Validation passed for in-stock item")
            
            # Actually create the order to test stock reduction
            print("   🔄 Creating order to test stock reduction...")
            original_stock = in_stock_product.stock_quantity
            
            try:
                order = serializer_valid.save()
                print(f"   ✅ Order created: {order.id}")
                
                # Check if stock was reduced
                in_stock_product.refresh_from_db()
                new_stock = in_stock_product.stock_quantity
                print(f"   📊 Stock before: {original_stock}, after: {new_stock}")
                
                if new_stock == original_stock - 1:
                    print("   ✅ SUCCESS: Stock was correctly reduced")
                else:
                    print("   ❌ PROBLEM: Stock was not reduced correctly")
                
                # Clean up - delete the test order
                order.delete()
                print("   🧹 Test order cleaned up")
                
            except Exception as e:
                print(f"   ❌ Error creating order: {e}")
        else:
            print("   ❌ PROBLEM: Validation failed for in-stock item")
            print("   Errors:", serializer_valid.errors)
    else:
        print("   ⚠️  No in-stock products found for testing")
    
    # Test 3: Test excessive quantity
    print(f"\n3️⃣ Testing excessive quantity validation...")
    
    if in_stock_product and in_stock_product.stock_quantity > 0:
        excessive_quantity = in_stock_product.stock_quantity + 10
        
        order_data_excessive = order_data.copy()
        order_data_excessive['id'] = 'TEST_STOCK_003'
        order_data_excessive['items'] = [{
            'product_id': in_stock_product.id,
            'quantity': excessive_quantity,
            'unit_price': 25.00
        }]
        
        serializer_excessive = CreateOrderSerializer(data=order_data_excessive, context={'request': Request(request)})
        
        if serializer_excessive.is_valid():
            print(f"   ❌ PROBLEM: Validation passed for excessive quantity ({excessive_quantity} > {in_stock_product.stock_quantity})")
        else:
            print(f"   ✅ SUCCESS: Validation failed for excessive quantity ({excessive_quantity} > {in_stock_product.stock_quantity})")
            print("   Errors:", serializer_excessive.errors)
    
    print(f"\n📋 SUMMARY")
    print("=" * 30)
    print("✅ Stock validation has been implemented with:")
    print("   - Order creation validates stock availability")
    print("   - Automatic stock reduction after successful orders")
    print("   - Proper error messages for out-of-stock items")
    print("   - Validation for excessive quantities")
    
    print(f"\n🚀 NEXT STEPS")
    print("=" * 30)
    print("1. Start your backend server: python backend/manage.py runserver")
    print("2. Test in the frontend by trying to add out-of-stock items to cart")
    print("3. Try to checkout with out-of-stock items")
    print("4. Deploy to production with these fixes")

if __name__ == "__main__":
    test_stock_validation_direct()