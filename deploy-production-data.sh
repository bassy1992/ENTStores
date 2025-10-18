#!/bin/bash

# Deploy production data to Railway
echo "🚀 Deploying to Railway with production data..."

# Commit the changes
git add .
git commit -m "Add production data deployment script"

# Push to Railway (assuming you have Railway CLI configured)
echo "📤 Pushing to Railway..."
git push origin main

echo "✅ Deployment initiated! Check Railway dashboard for progress."
echo "🌐 Your app will be available at: https://entstores-production.up.railway.app/"
echo "🔧 Admin panel: https://entstores-production.up.railway.app/admin/"