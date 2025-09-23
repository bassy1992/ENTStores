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
    echo "Creating media directory for Render..."
    mkdir -p /opt/render/project/data/media
    chmod 755 /opt/render/project/data/media
    echo "Created media directory at /opt/render/project/data/media"
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --no-input

# Show migration status for debugging
echo "Checking migration status..."
python manage.py showmigrations shop

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