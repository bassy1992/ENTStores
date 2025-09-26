# Stock Display Issue Fix

## Problem
Products with variants show as "Out of Stock" on the shop page even when variants have stock available. This happens because:

1. Main product has `stock_quantity: 0` and `is_in_stock: false`
2. Variants have `stock_quantity: 20` and `is_in_stock: true`
3. The backend's `is_in_stock` property only checks main product stock, not variant stock

## Root Cause
The `Product.is_in_stock` property in `backend/shop/models.py` only checks:
```python
@property
def is_in_stock(self):
    return self.stock_quantity > 0
```

It doesn't consider variant stock.

## Solution Applied

### 1. Backend Model Fix (models.py)
Updated the `is_in_stock` property to consider both main stock and variant stock:

```python
@property
def is_in_stock(self):
    """Check if product is in stock (considering both main stock and variants)"""
    # First check main product stock
    if self.stock_quantity > 0:
        return True
    
    # If main stock is 0, check if any variants are in stock
    try:
        # Check if any variants have stock
        return self.variants.filter(
            stock_quantity__gt=0,
            is_available=True
        ).exists()
    except Exception:
        # If variants table doesn't exist or there's an error, fall back to main stock
        return self.stock_quantity > 0
```

### 2. Backend Serializer Fix (serializers.py)
Updated both `ProductSerializer` and `ProductFullSerializer` to use a method field:

```python
is_in_stock = serializers.SerializerMethodField()

def get_is_in_stock(self, obj):
    """Check if product is in stock (considering both main stock and variants)"""
    return obj.is_in_stock
```

### 3. Frontend Validation
The frontend already handles this correctly:
- Product detail page checks variant stock when variants are selected
- Shop page will now show correct stock status after backend fix
- Cart page allows items to be added (which is correct behavior)

## Deployment Steps

1. Deploy the updated backend code to production
2. Restart the production server
3. Test the specific product: https://www.enontinoclothingstore.com/product/shorts-coral-pink
4. Verify it now shows "In Stock" on the shop page
5. Verify variants still work correctly on the product detail page

## Testing
After deployment, the "SHORTS Coral Pink" product should:
- Show as "In Stock" on the shop page
- Allow adding to cart from the shop page
- Continue to work correctly on the product detail page with variant selection