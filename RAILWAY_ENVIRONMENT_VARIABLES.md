# Railway Environment Variables Setup

This document lists all environment variables needed for your Django backend on Railway.

## 🚀 Required Environment Variables

### **Core Django Settings**
```bash
# Django Secret Key (REQUIRED)
DJANGO_SECRET_KEY=your-super-secret-key-here-make-it-long-and-random

# Debug Mode (REQUIRED)
DEBUG=False

# Railway Environment Indicator (REQUIRED)
RAILWAY_ENVIRONMENT=production
```

### **Database Configuration**
```bash
# PostgreSQL Database URL (Auto-provided by Railway)
DATABASE_URL=postgresql://user:password@host:port/database

# Internal Database URL (Auto-provided by Railway)
DATABASE_INTERNAL_URL=postgresql://user:password@internal-host:port/database

# Force SQLite (Optional - set to 'true' only for testing)
USE_SQLITE=False
```

### **Domain and CORS Settings**
```bash
# Railway Public Domain (Auto-provided)
RAILWAY_PUBLIC_DOMAIN=your-app-name.up.railway.app

# Railway Static URL (Auto-provided)
RAILWAY_STATIC_URL=your-app-name.up.railway.app

# Frontend URL (Your Vercel/Netlify domain)
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

### **Payment Integration**
```bash
# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# MTN MoMo Configuration (Optional)
MOMO_SUBSCRIPTION_KEY=your_momo_subscription_key
MOMO_API_USER=your_momo_api_user
MOMO_API_KEY=your_momo_api_key
```

### **Email Configuration (Brevo SMTP)**
```bash
# Email Backend
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

# Brevo SMTP Credentials
EMAIL_HOST_USER=your-brevo-email@example.com
EMAIL_HOST_PASSWORD=your-brevo-smtp-password

# Email Addresses
DEFAULT_FROM_EMAIL=ENTstore <awuleynovember@gmail.com>
ADMIN_EMAIL=Enontinoclothing@gmail.com
```

### **File Storage (Optional)**
```bash
# GitHub Storage (for media files)
GITHUB_TOKEN=ghp_your_github_personal_access_token
GITHUB_MEDIA_REPO=ENTstore-media

# Cloudinary (Optional backup storage)
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
CLOUDINARY_CLOUD_NAME=entstore
```

## 🔧 How to Add Variables to Railway

### **Method 1: Railway Dashboard**
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Select your project
3. Click on your backend service
4. Go to **Variables** tab
5. Add each variable with **Key** and **Value**

### **Method 2: Railway CLI**
```bash
# Login to Railway
railway login

# Link to your project
railway link

# Add variables one by one
railway variables set DJANGO_SECRET_KEY="your-secret-key"
railway variables set DEBUG="False"
railway variables set RAILWAY_ENVIRONMENT="production"

# Or add multiple at once
railway variables set DJANGO_SECRET_KEY="your-key" DEBUG="False" RAILWAY_ENVIRONMENT="production"
```

### **Method 3: Environment File Upload**
Create a `.env.railway` file and upload it:
```bash
# Create the file
cat > .env.railway << 'EOF'
DJANGO_SECRET_KEY=your-super-secret-key-here
DEBUG=False
RAILWAY_ENVIRONMENT=production
STRIPE_PUBLISHABLE_KEY=pk_live_your_key
STRIPE_SECRET_KEY=sk_live_your_key
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=ENTstore <awuleynovember@gmail.com>
ADMIN_EMAIL=Enontinoclothing@gmail.com
FRONTEND_URL=https://your-frontend.vercel.app
EOF

# Upload using Railway CLI
railway variables --file .env.railway
```

## 🔐 Security Best Practices

### **Generate Secure Secret Key**
```python
# Run this in Python to generate a secure secret key
import secrets
import string

alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
secret_key = ''.join(secrets.choice(alphabet) for i in range(50))
print(f"DJANGO_SECRET_KEY={secret_key}")
```

### **Stripe Keys**
- Use **live keys** for production (`pk_live_...` and `sk_live_...`)
- Test with **test keys** first (`pk_test_...` and `sk_test_...`)

### **Email Configuration**
- Use your verified Brevo sender email
- Keep SMTP credentials secure

## 📋 Variable Checklist

Copy this checklist and check off each variable as you add it:

### **Essential (Required for basic functionality)**
- [ ] `DJANGO_SECRET_KEY`
- [ ] `DEBUG=False`
- [ ] `RAILWAY_ENVIRONMENT=production`
- [ ] `DATABASE_URL` (auto-provided by Railway)

### **Frontend Integration**
- [ ] `FRONTEND_URL`
- [ ] `RAILWAY_PUBLIC_DOMAIN` (auto-provided)

### **Payment Processing**
- [ ] `STRIPE_PUBLISHABLE_KEY`
- [ ] `STRIPE_SECRET_KEY`
- [ ] `STRIPE_WEBHOOK_SECRET`

### **Email Notifications**
- [ ] `EMAIL_HOST_USER`
- [ ] `EMAIL_HOST_PASSWORD`
- [ ] `DEFAULT_FROM_EMAIL`
- [ ] `ADMIN_EMAIL`

### **Optional Features**
- [ ] `GITHUB_TOKEN` (for media storage)
- [ ] `CLOUDINARY_API_KEY` (backup storage)
- [ ] `MOMO_SUBSCRIPTION_KEY` (MTN MoMo payments)

## 🧪 Testing Variables

After adding variables, test your deployment:

```bash
# Check if variables are set
railway variables

# View deployment logs
railway logs

# Test the application
curl https://your-app.up.railway.app/api/products/
```

## 🔄 Auto-Provided Variables

Railway automatically provides these variables:
- `DATABASE_URL` - PostgreSQL connection string
- `DATABASE_INTERNAL_URL` - Internal PostgreSQL connection
- `RAILWAY_STATIC_URL` - Your app's Railway domain
- `RAILWAY_PUBLIC_DOMAIN` - Public domain for your app
- `PORT` - Port number for your application

## 🚨 Common Issues

### **Secret Key Error**
```
Error: SECRET_KEY setting must not be empty
```
**Solution**: Add `DJANGO_SECRET_KEY` variable

### **Database Connection Error**
```
Error: could not connect to server
```
**Solution**: Ensure `DATABASE_URL` is set (usually auto-provided)

### **CORS Errors**
```
Error: CORS policy blocked
```
**Solution**: Add your frontend domain to `FRONTEND_URL`

### **Email Errors**
```
Error: SMTP authentication failed
```
**Solution**: Verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`

## 📞 Support

If you encounter issues:
1. Check Railway logs: `railway logs`
2. Verify all required variables are set
3. Test with minimal configuration first
4. Check Django settings for typos

---

**Next Steps**: After adding these variables, your Django backend will be fully configured for production on Railway! 🎉