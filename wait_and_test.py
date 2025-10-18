#!/usr/bin/env python
import requests
import time

def wait_and_test():
    """Wait for deployment and test the fix"""
    print("⏳ Waiting for deployment to complete...")
    
    for attempt in range(6):  # Try 6 times with 30 second intervals
        print(f"\n🔄 Attempt {attempt + 1}/6...")
        time.sleep(30 if attempt > 0 else 5)  # Wait 30 seconds between attempts
        
        try:
            # Test with cache busting
            timestamp = int(time.time())
            url = f"https://entstores-production.up.railway.app/api/shop/products/?_t={timestamp}"
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                coral_pink = None
                for product in results:
                    if 'coral' in product.get('title', '').lower() and 'pink' in product.get('title', '').lower():
                        coral_pink = product
                        break
                
                if coral_pink:
                    is_in_stock = coral_pink.get('is_in_stock', False)
                    stock_qty = coral_pink.get('stock_quantity', 0)
                    
                    print(f"📦 Product: {coral_pink.get('title')}")
                    print(f"📊 Stock Quantity: {stock_qty}")
                    print(f"✅ Is In Stock: {is_in_stock}")
                    
                    if is_in_stock:
                        print("\n🎉 SUCCESS! The fix has been deployed!")
                        print("✅ Shop page will now show the product as 'In Stock'")
                        print("🌐 Visit: https://www.enontinoclothingstore.com/product/shorts-coral-pink")
                        return True
                    else:
                        print("⏳ Still showing as out of stock, waiting for deployment...")
                else:
                    print("❌ Product not found in API response")
            else:
                print(f"❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n⚠️  Deployment may be taking longer than expected.")
    print("🔄 Try checking the site manually or run the test again later.")
    return False

if __name__ == "__main__":
    wait_and_test()