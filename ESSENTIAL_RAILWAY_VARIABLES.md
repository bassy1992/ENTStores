# Essential Railway Variables Quick Setup

## 🚀 Run the Setup Script
```bash
python add_railway_variables.py
```

## 📋 Essential Variables Checklist

### **Core Django (REQUIRED)**
```bash
DJANGO_SECRET_KEY=your-50-character-secret-key
DEBUG=False
RAILWAY_ENVIRONMENT=production
```

### **Stripe Payment (REQUIRED for checkout)**
```bash
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### **Email Configuration (REQUIRED for notifications)**
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=your-brevo-email@example.com
EMAIL_HOST_PASSWORD=your-brevo-smtp-password
DEFAULT_FROM_EMAIL=ENTstore <awuleynovember@gmail.com>
ADMIN_EMAIL=Enontinoclothing@gmail.com
```

### **Frontend Integration (REQUIRED for CORS)**
```bash
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

## 🔑 Where to Get Your Keys

### **Stripe Keys**
1. Go to [Stripe Dashboard](https://dashboard.stripe.com/apikeys)
2. Copy your **Publishable key** (starts with `pk_live_` or `pk_test_`)
3. Copy your **Secret key** (starts with `sk_live_` or `sk_test_`)
4. For webhook secret:
   - Go to [Webhooks](https://dashboard.stripe.com/webhooks)
   - Create endpoint: `https://your-railway-app.up.railway.app/api/stripe/webhook/`
   - Copy the **Signing secret** (starts with `whsec_`)

### **Brevo Email Keys**
1. Go to [Brevo SMTP Settings](https://app.brevo.com/settings/keys/smtp)
2. Copy your **Login** (email address)
3. Copy your **Password** (SMTP password)

## ⚡ Quick Manual Setup

If you prefer to set variables manually:

```bash
# Login to Railway
railway login

# Set core variables
railway variables set DJANGO_SECRET_KEY="your-secret-key"
railway variables set DEBUG="False"
railway variables set RAILWAY_ENVIRONMENT="production"

# Set Stripe variables
railway variables set STRIPE_PUBLISHABLE_KEY="pk_live_your_key"
railway variables set STRIPE_SECRET_KEY="sk_live_your_key"
railway variables set STRIPE_WEBHOOK_SECRET="whsec_your_secret"

# Set email variables
railway variables set EMAIL_HOST_USER="your-email@example.com"
railway variables set EMAIL_HOST_PASSWORD="your-password"
railway variables set DEFAULT_FROM_EMAIL="ENTstore <awuleynovember@gmail.com>"
railway variables set ADMIN_EMAIL="Enontinoclothing@gmail.com"

# Set frontend URL
railway variables set FRONTEND_URL="https://your-frontend.vercel.app"
```

## 🧪 Test Your Setup

After adding variables:

```bash
# Check variables are set
railway variables

# Redeploy your app
railway up

# Check logs
railway logs

# Test your API
curl https://your-app.up.railway.app/api/products/

# Test Stripe webhook
curl -X POST https://your-app.up.railway.app/api/stripe/webhook/
```

## 🔐 Security Notes

- **Use LIVE keys for production** (`pk_live_`, `sk_live_`)
- **Use TEST keys for testing** (`pk_test_`, `sk_test_`)
- **Keep secret keys secure** - never commit them to code
- **Regenerate keys if compromised**

## 🚨 Common Issues

### **Secret Key Error**
```
Error: SECRET_KEY setting must not be empty
```
**Solution**: Set `DJANGO_SECRET_KEY`

### **Stripe Error**
```
Error: No API key provided
```
**Solution**: Set `STRIPE_SECRET_KEY`

### **Email Error**
```
Error: SMTP authentication failed
```
**Solution**: Verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`

### **CORS Error**
```
Error: CORS policy blocked
```
**Solution**: Set `FRONTEND_URL` to your Vercel domain

## 📞 Need Help?

1. **Check Railway logs**: `railway logs`
2. **Verify variables**: `railway variables`
3. **Test endpoints**: Use curl or Postman
4. **Check Django admin**: `/admin/`

---

**After setup, your Railway backend will be fully configured for production! 🎉**