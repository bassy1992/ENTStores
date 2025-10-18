@echo off
REM Railway Variables Setup for Windows
REM Quick setup of essential environment variables

echo 🚀 Railway Variables Setup
echo ===========================

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Railway CLI not found!
    echo Install from: https://docs.railway.app/develop/cli
    echo.
    echo After installation, run:
    echo   railway login
    echo   railway link
    echo.
    pause
    exit /b 1
)

echo ✅ Railway CLI found

REM Check if logged in
railway whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Not logged in to Railway!
    echo Run: railway login
    pause
    exit /b 1
)

echo ✅ Logged in to Railway

echo.
echo 📝 Setting up essential variables...
echo.

REM Generate Django secret key
echo 🔐 Generating Django secret key...
python -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits + '!@#$%%^&*(-_=+)') for i in range(50)))" > temp_key.txt
set /p DJANGO_KEY=<temp_key.txt
del temp_key.txt

REM Set core Django variables
echo 📋 Setting core Django variables...
railway variables set DJANGO_SECRET_KEY="%DJANGO_KEY%"
railway variables set DEBUG="False"
railway variables set RAILWAY_ENVIRONMENT="production"
railway variables set USE_SQLITE="False"

echo.
echo ✅ Core variables set!
echo.

REM Prompt for Stripe keys
echo 💳 Stripe Configuration
echo Get your keys from: https://dashboard.stripe.com/apikeys
echo.
set /p STRIPE_PUB="Enter Stripe Publishable Key (pk_live_... or pk_test_...): "
set /p STRIPE_SECRET="Enter Stripe Secret Key (sk_live_... or sk_test_...): "
set /p STRIPE_WEBHOOK="Enter Stripe Webhook Secret (whsec_...): "

if not "%STRIPE_PUB%"=="" (
    railway variables set STRIPE_PUBLISHABLE_KEY="%STRIPE_PUB%"
    echo ✅ Stripe publishable key set
)

if not "%STRIPE_SECRET%"=="" (
    railway variables set STRIPE_SECRET_KEY="%STRIPE_SECRET%"
    echo ✅ Stripe secret key set
)

if not "%STRIPE_WEBHOOK%"=="" (
    railway variables set STRIPE_WEBHOOK_SECRET="%STRIPE_WEBHOOK%"
    echo ✅ Stripe webhook secret set
)

echo.
REM Prompt for email configuration
echo 📧 Email Configuration (Brevo SMTP)
echo Get credentials from: https://app.brevo.com/settings/keys/smtp
echo.
set /p EMAIL_USER="Enter Brevo Email/Username: "
set /p EMAIL_PASS="Enter Brevo SMTP Password: "

if not "%EMAIL_USER%"=="" if not "%EMAIL_PASS%"=="" (
    railway variables set EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
    railway variables set EMAIL_HOST_USER="%EMAIL_USER%"
    railway variables set EMAIL_HOST_PASSWORD="%EMAIL_PASS%"
    railway variables set DEFAULT_FROM_EMAIL="ENTstore <awuleynovember@gmail.com>"
    railway variables set ADMIN_EMAIL="Enontinoclothing@gmail.com"
    echo ✅ Email configuration set
)

echo.
REM Prompt for frontend URL
echo 🌐 Frontend Integration
set /p FRONTEND_URL="Enter Frontend URL (e.g., https://your-app.vercel.app): "

if not "%FRONTEND_URL%"=="" (
    railway variables set FRONTEND_URL="%FRONTEND_URL%"
    echo ✅ Frontend URL set
)

echo.
echo 🎉 Railway variables setup complete!
echo.
echo 📋 Next Steps:
echo   1. Check variables: railway variables
echo   2. Deploy your app: railway up
echo   3. Check logs: railway logs
echo   4. Test your API endpoints
echo.
echo 🔍 Verification:
echo   - API: https://your-app.up.railway.app/api/products/
echo   - Admin: https://your-app.up.railway.app/admin/
echo.
pause