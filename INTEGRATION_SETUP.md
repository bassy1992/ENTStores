# Frontend-Backend Integration Setup

This guide explains how to connect the frontend shop page to the Django backend database.

## Backend Setup (Django API)

1. **Start the Django server:**
   ```bash
   cd backend
   python manage.py runserver 8000
   ```

2. **Verify the API is working:**
   - Open `backend/test_api.html` in your browser
   - Or visit: http://localhost:8000/api/shop/products/
   - You should see JSON data with products from the database

3. **Available API endpoints:**
   - `GET /api/shop/categories/` - All categories
   - `GET /api/shop/categories/featured/` - Featured categories only
   - `GET /api/shop/products/` - All products (with filtering)
   - `GET /api/shop/products/featured/` - Featured products only
   - `GET /api/shop/products/<slug>/` - Single product by slug
   - `GET /api/shop/search/?q=<query>` - Search products
   - `GET /api/shop/stats/` - Shop statistics

## Frontend Setup (React/Vite)

1. **Start the frontend server:**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Visit the shop page:**
   - Go to: http://localhost:8080/shop
   - The page should now load products from the Django database
   - Categories should also be loaded from the API

## What Changed

### New Files:
- `frontend/client/services/api.ts` - API service functions
- `backend/shop/serializers.py` - DRF serializers
- `backend/shop/views.py` - API views
- `backend/shop/urls.py` - API URL patterns

### Updated Files:
- `frontend/client/pages/Shop.tsx` - Now uses API instead of static data
- `frontend/client/components/shop/CategoryPills.tsx` - Loads categories from API
- `frontend/client/pages/Home.tsx` - Loads featured products from API
- `backend/myproject/settings.py` - Added DRF and CORS settings
- `backend/myproject/urls.py` - Added shop API URLs

## Features

### Shop Page (`/shop`)
- ✅ Loads all products from database
- ✅ Category filtering works with API
- ✅ Loading states and error handling
- ✅ Empty state when no products found

### Home Page (`/`)
- ✅ Featured products loaded from API
- ✅ Loading skeleton while fetching data

### Category Pills
- ✅ Categories loaded from database
- ✅ Loading state with skeleton
- ✅ Fallback to empty array if API fails

## API Response Format

### Products:
```json
{
  "count": 13,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "track-jacket-sky",
      "title": "ENNC Track Jacket — Sky",
      "slug": "ennc-track-jacket-sky",
      "price": 7500,
      "price_display": "$75.00",
      "description": "Lightweight track jacket...",
      "image": "https://cdn.builder.io/...",
      "category": "tracksuits",
      "category_label": "Tracksuits",
      "stock_quantity": 25,
      "is_active": true,
      "is_in_stock": true,
      "tags": ["featured", "new"],
      "created_at": "2025-09-17T10:11:20.123456Z"
    }
  ]
}
```

### Categories:
```json
[
  {
    "key": "t-shirts",
    "label": "T-Shirts",
    "description": "Premium cotton tees...",
    "image": "https://cdn.builder.io/...",
    "featured": true,
    "product_count": 2
  }
]
```

## Troubleshooting

### CORS Issues
If you get CORS errors, make sure:
1. Django server is running on port 8000
2. Frontend is running on port 8080 or 5173
3. CORS settings in `backend/myproject/settings.py` include your frontend URL

### API Not Loading
1. Check Django server is running: http://localhost:8000/api/shop/products/
2. Check browser console for errors
3. Verify database has data: `python manage.py populate_shop_data`

### Empty Product List
1. Run: `python manage.py populate_shop_data` to add sample data
2. Check Django admin: http://localhost:8000/admin/ (admin/admin123)
3. Verify products are active and have stock

## Next Steps

The integration is now complete! The shop page loads products from your Django database instead of static data. You can:

1. Add more products through Django admin
2. Create new categories
3. Update product information
4. All changes will be reflected immediately on the frontend

The API supports filtering, searching, and pagination for future enhancements.