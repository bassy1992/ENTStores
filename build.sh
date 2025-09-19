#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

echo "Navigating to backend directory..."
cd backend

echo "Creating staticfiles directory..."
mkdir -p staticfiles

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Running database migrations..."
python manage.py migrate

echo "Listing static files..."
ls -la staticfiles/

echo "Build completed successfully!"
cd ..