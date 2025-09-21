#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Navigate to backend directory
cd backend

# Create media directory if it doesn't exist (for Render persistent disk)
if [ "$RENDER" = "true" ]; then
    mkdir -p /opt/render/project/data/media
    echo "Created media directory at /opt/render/project/data/media"
fi

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

echo "Build completed successfully!"