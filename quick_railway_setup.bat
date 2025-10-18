@echo off
REM Quick Railway Environment Variables Setup
REM This script sets up essential variables for Railway deployment

echo 🚀 Quick Railway Environment Variables Setup
echo =============================================

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Railway CLI not found!
    echo Install it from: https://docs.railway.app/develop/cli
    pause
    exit /b 1
)

echo ✅ Railway CLI found

REM Generate a secure Django secret key
echo 🔐 Generating secure Django secret key...
python -c "import secrets, string; print('DJANGO_SECRET_KEY=' + ''.join(secrets.choice(string.ascii_letters + string.digits + '!@#$%%^&*(-_=+)') for i in range(50)))" > temp_secret.txt
set /p SECRET_KEY=<temp_secret.txt
del temp_secret.txt

echo ✅ Generated secret key

REM Set core variables
echo 📝 Setting core Django variables...
railway variables set %SECRET_KEY%
railway variables set DEBUG="False"
railway variables set RAILWAY_ENVIRONMENT="production"

echo ✅ Core variables set

REM Set email variables (using default ENT store emails)
echo 📧 Setting default email configuration...
railway variables set EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
railway variables set DEFAULT_FROM_EMAIL="ENTstore <awuleynovember@gmail.com>"
railway variables set ADMIN_EMAIL="Enontinoclothing@gmail.com"

echo ✅ Email configuration set

echo.
echo 🎉 Basic Railway setup complete!
echo.
echo ⚠️  You still need to add:
echo   - EMAIL_HOST_USER (your Brevo email)
echo   - EMAIL_HOST_PASSWORD (your Brevo SMTP password)
echo   - STRIPE_PUBLISHABLE_KEY (your Stripe public key)
echo   - STRIPE_SECRET_KEY (your Stripe secret key)
echo   - FRONTEND_URL (your Vercel/Netlify domain)
echo.
echo 🔧 Add these manually in Railway dashboard or use:
echo   railway variables set EMAIL_HOST_USER="your-email@example.com"
echo   railway variables set EMAIL_HOST_PASSWORD="your-password"
echo.
echo 📋 Check all variables: railway variables
echo 🚀 Deploy your app: railway up
echo 📊 View logs: railway logs
echo.
pause