#!/bin/bash

# Railway Deployment Script for Django Backend

echo "🚀 Starting Railway deployment..."

# Install Railway CLI if not installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway (if not already logged in)
echo "Please make sure you're logged in to Railway..."
railway login

# Link to your Railway project (you'll need to run this once)
echo "Linking to Railway project..."
railway link

# Set environment variables on Railway
echo "Setting environment variables..."

# Production settings
railway variables set DEBUG=False
railway variables set DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"

# Database (Railway will provide this automatically if you have a PostgreSQL service)
# railway variables set DATABASE_URL="your_railway_postgres_url"

# Stripe settings (replace with your production keys)
railway variables set STRIPE_PUBLISHABLE_KEY="pk_test_your_stripe_publishable_key_here"
railway variables set STRIPE_SECRET_KEY="sk_test_your_stripe_secret_key_here"

# Email settings
railway variables set EMAIL_HOST_USER="your_email_host_user@smtp-brevo.com"
railway variables set EMAIL_HOST_PASSWORD="your_email_host_password_here"

# Frontend URL (update this with your actual Vercel URL)
railway variables set FRONTEND_URL="https://enintino.vercel.app"

# Deploy to Railway
echo "Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "Your backend should be available at your Railway domain."