#!/bin/bash

# Deploy script for production with live Stripe keys
echo "🚀 Deploying to production with live Stripe keys..."

echo "📋 Environment Variables to set in Render Backend:"
echo "STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_ACTUAL_LIVE_PUBLISHABLE_KEY"
echo "STRIPE_SECRET_KEY=sk_live_YOUR_ACTUAL_LIVE_SECRET_KEY"
echo ""
echo "📋 Environment Variables to set in Vercel Frontend:"
echo "VITE_STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_ACTUAL_LIVE_PUBLISHABLE_KEY"
echo ""
echo "⚠️  NEXT STEPS:"
echo "1. Set up live webhook in Stripe Dashboard"
echo "2. Webhook URL: https://entstores.onrender.com/api/payments/stripe/webhook/"
echo "3. Add webhook secret to STRIPE_WEBHOOK_SECRET"
echo "4. Test payment flow thoroughly"
echo ""
echo "✅ Live Stripe keys ready for deployment!"