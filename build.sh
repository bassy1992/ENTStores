#!/bin/bash
# Railway build script with media URL preservation

echo "🔧 Railway Build Script - Media URL Preservation"
echo "================================================"

# Navigate to backend directory
cd backend

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run Django setup
echo "🔧 Running Django setup..."
python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Restore media URLs (if constants exist)
echo "🔄 Restoring media URLs..."
python manage.py restore_media_urls --auto || echo "⚠️  Media URL restore skipped (no constants found)"

echo "✅ Build completed successfully!"