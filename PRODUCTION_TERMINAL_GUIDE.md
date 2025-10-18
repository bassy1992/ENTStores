# Production Terminal Access Guide

You now have direct terminal access to your Railway production database! Here's how to use it.

## 🚀 Quick Start

### Basic Commands
```bash
# Show database statistics
prod stats

# List products
prod products

# Show detailed database info
prod info

# Django shell with production data
prod shell
```

### Management Commands
```bash
# Run migrations
prod migrate

# Create database backup
prod backup

# Update existing products with URL images
prod update-images

# Load sample products
prod load-samples
```

## 📁 Files Created

### Main Scripts
- **`prod.bat`** - Main command interface (Windows)
- **`prod_local.py`** - Quick database access and stats
- **`prod_manage_local.py`** - Comprehensive database management

### Legacy Scripts (if needed)
- **`prod_shell.py`** - Django shell access
- **`prod_dbshell.py`** - Direct PostgreSQL shell
- **`prod_utils.py`** - Database utilities

## 🔧 How It Works

### Database Connection
- Uses your existing `DATABASE_URL` environment variable
- Connects to Railway's external PostgreSQL endpoint
- No need for Railway CLI or special authentication

### Smart Configuration
- Automatically detects local vs Railway environment
- Uses external URL for local access
- Uses internal URL when running on Railway

## 📊 Common Tasks

### Check Database Status
```bash
prod info
```
Shows:
- Database connection details
- Table counts
- Image statistics
- Recent orders

### Manage Products
```bash
# List all products
prod products

# Update products to use URL images
prod update-images

# Add sample products with URLs
prod load-samples
```

### Database Operations
```bash
# Run migrations
prod migrate

# Create backup
prod backup

# Interactive Django shell
prod shell
```

### In Django Shell
```python
# List products with URL images
Product.objects.filter(image_url__isnull=False)

# Update a product's image URL
product = Product.objects.get(id='your-product-id')
product.image_url = 'https://your-image-url.com/image.jpg'
product.save()

# Create a new product
Product.objects.create(
    id='new-product',
    title='New Product',
    price='29.99',
    description='Product description',
    image_url='https://images.unsplash.com/photo-123?w=400&h=400',
    category=Category.objects.get(key='t-shirts'),
    stock_quantity=10,
    is_active=True
)
```

## 🛠️ Advanced Usage

### Direct Django Management
```bash
# Any Django management command
python prod_manage_local.py <django-command>

# Examples:
python prod_manage_local.py showmigrations
python prod_manage_local.py createsuperuser
python prod_manage_local.py collectstatic
```

### Database Shell Access
```bash
# PostgreSQL shell (if needed)
python prod_dbshell.py
```

### Custom Scripts
You can create your own scripts using this pattern:
```python
import os
import sys
import django

# Setup
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Your code here
from shop.models import Product
products = Product.objects.all()
```

## 🔍 Troubleshooting

### Connection Issues
If you get connection errors:
1. Check your `DATABASE_URL` environment variable
2. Ensure it's the external Railway URL (not internal)
3. Verify Railway database is running

### Environment Variables
Make sure you have:
```bash
DATABASE_URL=postgresql://user:pass@host:port/database
```

### Permission Issues
If you get permission errors:
1. Ensure your Railway database user has proper permissions
2. Check if the database allows external connections

## 📈 Monitoring

### Regular Checks
```bash
# Daily database health check
prod info

# Weekly backup
prod backup

# Monitor product images
prod stats
```

### Performance
- All operations use the same connection as your app
- No additional load on Railway infrastructure
- Direct PostgreSQL access for complex queries

## 🎯 Best Practices

### Data Safety
- Always backup before major changes: `prod backup`
- Test changes in Django shell first
- Use transactions for bulk operations

### Image Management
- Prefer URL images over file uploads
- Use CDN services for better performance
- Update existing products: `prod update-images`

### Development Workflow
1. Make changes locally using production data
2. Test thoroughly in Django shell
3. Deploy code changes to Railway
4. Verify in production

## 🚀 Next Steps

Now that you have production access:

1. **Update Product Images**: Run `prod update-images` to convert existing products to URL images
2. **Add New Products**: Use `prod shell` to add products with URL images
3. **Monitor Performance**: Regular `prod info` checks
4. **Backup Regularly**: Use `prod backup` for data safety

You're all set to manage your production database directly from the terminal! 🎉