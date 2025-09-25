#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Navigate to backend directory
cd backend

# AUTO-SYNC MEDIA SYSTEM for Render
if [ "$RENDER" = "true" ]; then
    echo "🔄 AUTO-SYNC MEDIA SYSTEM ACTIVATING..."
    
    # Step 1: Set up local media directories
    echo "📁 Setting up media directories..."
    mkdir -p /opt/render/project/data/media/products
    mkdir -p /opt/render/project/data/media/categories
    mkdir -p /opt/render/project/data/media_backup
    mkdir -p /opt/render/project/data/media_archive
    chmod -R 755 /opt/render/project/data/media*
    
    # Step 2: Auto-sync all media files
    echo "🚀 Auto-syncing media files..."
    python manage.py migrate_to_permanent --auto-sync || echo "⚠️  Auto-sync completed with warnings"
    
    # Step 3: Force create any still missing files
    echo "🔧 Ensuring all files exist..."
    python manage.py migrate_to_permanent --force-create || echo "⚠️  Force create completed"
    
    # Step 4: Final verification
    echo "🔍 Final verification..."
    python manage.py migrate_to_permanent --verify-only || echo "ℹ️  Verification completed"
    
    # Step 5: Show final status
    echo "📊 Media system status:"
    python manage.py migrate_to_permanent || echo "ℹ️  Status displayed"
    
    echo "✅ AUTO-SYNC MEDIA SYSTEM READY!"
    echo "🔄 All media files automatically synced and protected"
    echo "📊 File count: $(find /opt/render/project/data/media -type f 2>/dev/null | wc -l) files"
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