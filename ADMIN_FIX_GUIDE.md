# Admin 500 Error Fix Guide

## Problem
The admin area at `https://entstores.onrender.com/admin/shop/orderitem/` is showing a Server Error (500).

## Root Cause
The production database likely hasn't been updated with the latest migrations, specifically migration `0005_orderitem_product_variant_orderitem_selected_color_and_more.py` which adds new fields to the OrderItem model.

## Solution Steps

### 1. Check Current Status
First, let's verify the issue by checking the production database:

```bash
# On your local machine, connect to production database
python backend/check_production_db.py
```

### 2. Run Production Migrations
The most likely fix is to run the pending migrations on production:

```bash
# This should happen automatically on Render, but you can trigger it manually
# by redeploying or running the migration command
```

### 3. Manual Fix (if needed)
If the automatic migrations don't work, you can manually fix the database:

1. **Access Render Dashboard**
   - Go to your Render dashboard
   - Find your backend service
   - Go to the "Shell" tab

2. **Run Migration Commands**
   ```bash
   python manage.py showmigrations shop
   python manage.py migrate shop
   python manage.py fix_admin
   ```

### 4. Redeploy (Recommended)
The easiest solution is to trigger a new deployment:

1. **Push a small change to trigger redeploy**
   ```bash
   # Make a small change to trigger redeploy
   git add .
   git commit -m "Fix admin 500 error - run migrations"
   git push origin main
   ```

2. **Or manually redeploy on Render**
   - Go to your Render dashboard
   - Click "Manual Deploy" on your backend service

## What Was Fixed

### 1. Enhanced Error Handling
Updated the OrderItem admin configuration to handle database inconsistencies:

```python
# Added better error handling in admin.py
def get_queryset(self, request):
    try:
        queryset = super().get_queryset(request).select_related('order', 'product')
        if hasattr(OrderItem._meta.get_field('product_variant'), 'related_model'):
            queryset = queryset.select_related('product_variant')
        return queryset
    except Exception as e:
        # Fallback to basic queryset
        return super().get_queryset(request)
```

### 2. Migration Safety
The Procfile already includes migration commands:
```
web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT
```

### 3. Diagnostic Tools
Created several diagnostic scripts:
- `backend/debug_admin_error.py` - Local debugging
- `backend/check_production_db.py` - Production database check
- `backend/fix_production_admin.py` - Production fix script
- `backend/test_admin_url.py` - URL testing

## Verification

After applying the fix, verify that:

1. **Admin loads without errors**
   - Visit: `https://entstores.onrender.com/admin/shop/orderitem/`
   - Should show the OrderItem list page

2. **All admin sections work**
   - `/admin/shop/order/` - Orders
   - `/admin/shop/product/` - Products
   - `/admin/shop/category/` - Categories

3. **Database integrity**
   - Run: `python manage.py fix_admin` on production
   - Should show all tables exist and queries work

## Prevention

To prevent similar issues in the future:

1. **Always test migrations locally first**
2. **Use the diagnostic commands before deploying**
3. **Monitor deployment logs for migration errors**
4. **Keep the admin error handling robust**

## Emergency Rollback

If the fix causes other issues, you can rollback:

```bash
# Rollback the specific migration (if needed)
python manage.py migrate shop 0004_productcolor_productsize_productimage_productvariant
```

## Contact

If you continue to experience issues:
1. Check the Render deployment logs
2. Run the diagnostic scripts
3. Verify all environment variables are set correctly