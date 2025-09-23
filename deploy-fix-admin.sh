#!/bin/bash

# Deploy script to fix admin issues on production
echo "🚀 Deploying admin fixes to production..."

# Navigate to backend directory
cd backend

# Run migrations on production database
echo "📋 Running database migrations..."
python fix_production_admin.py

echo "✅ Admin fixes deployed successfully!"
echo "🌐 Check your admin at: https://entstores.onrender.com/admin/shop/orderitem/"