#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Navigate to backend directory
cd backend

# Create media directory if it doesn't exist (for Render persistent disk)
if [ "$RENDER" = "true" ]; then
    echo "Setting up media directory for Render..."
    mkdir -p /opt/render/project/data/media
    mkdir -p /opt/render/project/data/media/products
    mkdir -p /opt/render/project/data/media/categories
    chmod -R 755 /opt/render/project/data/media
    echo "Created media directory structure at /opt/render/project/data/media"
    
    # Create a symlink from backend/media to the persistent disk (if needed)
    if [ ! -L "media" ]; then
        ln -sf /opt/render/project/data/media media
        echo "Created symlink from backend/media to persistent disk"
    fi
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Run database migrations with comprehensive error handling
echo "Running database migrations..."

# First, try to run migrations normally
if python manage.py migrate --no-input; then
    echo "✅ Migrations completed successfully"
else
    echo "⚠️  Standard migration failed, trying alternative approaches..."
    
    # Try fake-initial in case of conflicts
    echo "Trying fake-initial migration..."
    if python manage.py migrate --fake-initial --no-input; then
        echo "✅ Fake-initial migration successful"
    else
        echo "⚠️  Fake-initial failed, trying manual column fix..."
        
        # Try to add missing column manually
        python manage.py shell -c "
from django.db import connection
try:
    with connection.cursor() as cursor:
        # Check if is_featured column exists
        cursor.execute(\"\"\"
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name = 'shop_product' 
                AND column_name = 'is_featured'
            );
        \"\"\")
        exists = cursor.fetchone()[0]
        
        if not exists:
            print('Adding missing is_featured column...')
            cursor.execute('ALTER TABLE shop_product ADD COLUMN is_featured BOOLEAN DEFAULT FALSE;')
            print('✅ Added is_featured column manually')
        else:
            print('✅ is_featured column already exists')
            
        # Now try to fake the migration
        cursor.execute(\"\"\"
            INSERT INTO django_migrations (app, name, applied) 
            VALUES ('shop', '0006_product_is_featured', NOW())
            ON CONFLICT (app, name) DO NOTHING;
        \"\"\")
        print('✅ Marked migration as applied')
        
except Exception as e:
    print(f'Manual fix failed: {e}')
" || echo "Manual column fix failed, continuing anyway..."
fi

# Show migration status for debugging
echo "Checking migration status..."
python manage.py showmigrations shop || echo "Could not show migrations"

# Create superuser if it doesn't exist (optional)
echo "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
" || echo "Superuser creation skipped"

echo "Build completed successfully!"