@echo off
echo 🔧 Setting up Stripe keys for Railway deployment
echo.

echo ⚠️  You need to get your Stripe keys from: https://dashboard.stripe.com/apikeys
echo.

echo 📝 Run these commands with your actual Stripe keys:
echo.
echo railway variables set STRIPE_PUBLISHABLE_KEY="pk_test_YOUR_ACTUAL_PUBLISHABLE_KEY"
echo railway variables set STRIPE_SECRET_KEY="sk_test_YOUR_ACTUAL_SECRET_KEY"
echo railway variables set STRIPE_WEBHOOK_SECRET="whsec_YOUR_ACTUAL_WEBHOOK_SECRET"
echo.

echo 🔄 After setting the variables, redeploy:
echo railway up
echo.

echo 🧪 Then test the payment endpoint:
echo curl https://entstores-production.up.railway.app/api/payments/test/
echo.

pause