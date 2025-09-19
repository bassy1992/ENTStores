#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

# Install Python dependencies
pip install -r backend/requirements.txt

# Navigate to backend directory
cd backend

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate