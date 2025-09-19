#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "=== Starting Render Build Process ==="

echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

echo "Navigating to backend directory..."
cd backend

echo "Python version:"
python --version

echo "Django version:"
python -c "import django; print(django.get_version())"

echo "Creating staticfiles directory..."
mkdir -p staticfiles

echo "Checking Django settings..."
python manage.py check --deploy

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear --verbosity=2

echo "Running database migrations..."
python manage.py migrate

echo "Checking static files structure..."
if [ -d "staticfiles" ]; then
    echo "Static files directory exists"
    echo "Contents of staticfiles:"
    ls -la staticfiles/
    if [ -d "staticfiles/admin" ]; then
        echo "Admin static files found:"
        ls -la staticfiles/admin/
    else
        echo "WARNING: Admin static files not found!"
    fi
else
    echo "ERROR: Static files directory not created!"
fi

echo "=== Build completed successfully! ==="
cd ..