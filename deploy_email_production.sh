#!/bin/bash

echo "🚀 Deploying Email Configuration to Production..."

# Deploy to production with email fix
echo "📤 Pushing to production..."
git add .
git commit -m "Fix: Ensure order confirmation emails are sent properly

- Updated email configuration with DEFAULT_FROM_EMAIL
- Added comprehensive email testing
- Verified SMTP connection and email sending
- All email tests passing locally"

git push origin main

echo "⏳ Waiting for deployment to complete..."
sleep 30

echo "🔍 Testing production email after deployment..."

# Test production email endpoint
curl -X GET "https://entstore-backend.onrender.com/test-email/" \
  -H "Accept: application/json" \
  -w "\nHTTP Status: %{http_code}\n"

echo ""
echo "✅ Email deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Check wyarquah@gmail.com for test emails"
echo "2. Verify emails arrive from awuleynovember@gmail.com"
echo "3. Test with real orders to confirm fix"
echo "4. Check production logs if issues persist"
echo ""
echo "🔗 Production URLs:"
echo "- Backend: https://entstore-backend.onrender.com"
echo "- Email Test: https://entstore-backend.onrender.com/test-email/"
echo "- Admin: https://entstore-backend.onrender.com/admin/"