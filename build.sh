#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

# Install Python dependencies from backend directory
pip install -r backend/requirements.txt

# Navigate to backend directory for Django commands
cd backend

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate

# Go back to root for deployment
cd ..