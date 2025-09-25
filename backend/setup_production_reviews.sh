#!/bin/bash

# Setup review system in production
echo "🚀 Setting up review system in production..."

# Run migrations
echo "📋 Running migrations..."
python manage.py makemigrations shop
python manage.py migrate

# Setup reviews
echo "📝 Setting up reviews..."
python manage.py setup_reviews

echo "✅ Review system setup completed!"
echo "🔗 Check admin at: /admin/shop/productreview/"