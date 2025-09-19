# ENNC Shop Backend

Django REST API backend for the ENNC e-commerce shop.

## Features

- **Categories**: Product categories with featured status
- **Products**: Full product catalog with images, pricing, and inventory
- **Tags**: Product tagging system (featured, new, bestseller, etc.)
- **Orders**: Order management with customer details and line items
- **Admin Interface**: Django admin for managing all data
- **REST API**: Full API for frontend integration

## Models

### Category
- Categories for organizing products (t-shirts, hoodies, etc.)
- Featured categories for homepage display
- Auto-calculated product counts

### Product
- Complete product information (title, price, description, images)
- Stock quantity tracking
- Slug-based URLs
- Category relationships

### ProductTag & ProductTagAssignment
- Flexible tagging system
- Support for featured, new, bestseller tags
- Many-to-many relationship with products

### Order & OrderItem
- Complete order tracking
- Customer information
- Shipping details
- Payment method tracking
- Line item details

## API Endpoints

### Categories
- `GET /api/shop/categories/` - List all categories
- `GET /api/shop/categories/featured/` - List featured categories

### Products
- `GET /api/shop/products/` - List products (with filtering)
- `GET /api/shop/products/featured/` - List featured products
- `GET /api/shop/products/<slug>/` - Get product details
- `GET /api/shop/search/?q=<query>` - Search products

### Orders
- `POST /api/shop/orders/` - Create new order
- `GET /api/shop/orders/<id>/` - Get order details

### Other
- `GET /api/shop/stats/` - Get shop statistics
- `GET /api/shop/tags/` - List all product tags

## Query Parameters

### Products endpoint supports:
- `category` - Filter by category key
- `tags` - Filter by tag names (comma-separated)
- `search` - Search in title and description
- `in_stock` - Filter by stock availability

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create superuser:
```bash
python manage.py create_superuser
```

4. Populate with sample data:
```bash
python manage.py populate_shop_data
```

5. Run development server:
```bash
python manage.py runserver
```

## Admin Access

- URL: http://localhost:8000/admin/
- Username: admin
- Password: admin123

## API Base URL

http://localhost:8000/api/shop/

## Frontend Integration

The API is configured with CORS to allow requests from:
- http://localhost:3000 (React dev server)
- http://localhost:5173 (Vite dev server)

## Data Population

The `populate_shop_data` management command creates:
- 9 product categories
- 4 product tags (featured, new, bestseller, sale)
- 13 sample products with realistic data
- Proper relationships and stock quantities

All data matches the frontend product catalog for seamless integration.