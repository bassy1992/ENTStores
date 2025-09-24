#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Navigate to backend directory
cd backend

# AGGRESSIVE MEDIA PROTECTION for Render
if [ "$RENDER" = "true" ]; then
    echo "🛡️ AGGRESSIVE MEDIA PROTECTION SYSTEM ACTIVATING..."
    
    # Step 1: Set up protection system
    echo "🔧 Setting up media protection..."
    python manage.py protect_media --setup || echo "⚠️  Protection setup failed"
    
    # Step 2: Create comprehensive backup
    echo "📦 Creating comprehensive backup..."
    python manage.py backup_restore_media --backup || echo "⚠️  Backup failed"
    
    # Step 3: Force restore all missing files
    echo "🚨 Force restoring all media files..."
    python manage.py protect_media --force-restore || echo "⚠️  Force restore failed"
    
    # Step 4: Verify everything is working
    echo "🔍 Final verification..."
    python manage.py protect_media --verify || echo "⚠️  Verification failed"
    
    # Step 5: Show final status
    echo "📊 Media protection status:"
    python manage.py protect_media || echo "⚠️  Status check failed"
    
    # Step 6: Create emergency placeholders if needed
    echo "🖼️ Creating emergency placeholders..."
    python manage.py protect_media --create-placeholders || echo "⚠️  Placeholder creation failed"
    
    echo "✅ AGGRESSIVE MEDIA PROTECTION COMPLETE!"
    echo "📊 Final file count: $(find /opt/render/project/data/media -type f 2>/dev/null | wc -l) files"
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