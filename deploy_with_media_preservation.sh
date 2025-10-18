#!/bin/bash
# Railway Deployment Script with Automatic Media URL Preservation
echo "🚀 Starting Railway deployment with media URL preservation..."

# Step 1: Backup current media URLs
echo "📦 Backing up media URLs..."
cd backend
python manage.py backup_media_urls --env-format

# Step 2: Deploy to Railway
echo "🚀 Deploying to Railway..."
cd ..
railway up

# Step 3: Wait for deployment
echo "⏳ Waiting for deployment to be ready..."
sleep 30

# Step 4: Restore media URLs (this happens automatically via auto_restore app)
echo "✅ Deployment complete! Media URLs will be restored automatically."
echo "🔗 Check your site: https://entstores-production.up.railway.app"
