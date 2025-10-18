# Railway Dashboard Variables Setup

Since you don't have Railway CLI installed locally, here's how to add all essential variables through the Railway dashboard.

## 🌐 Railway Dashboard Method

### **Step 1: Access Railway Dashboard**
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Login to your account
3. Select your project
4. Click on your **backend service**
5. Go to the **Variables** tab

### **Step 2: Add Essential Variables**

Click **"New Variable"** for each of these:

## 🔧 **Core Django Settings (REQUIRED)**

```
Key: DJANGO_SECRET_KEY
Value: [Generate a 50-character random string]
```

```
Key: DEBUG
Value: False
```

```
Key: RAILWAY_ENVIRONMENT
Value: production
```

```
Key: USE_SQLITE
Value: False
```

## 💳 **Stripe Payment Configuration**

Get your keys from [Stripe Dashboard](https://dashboard.stripe.com/apikeys):

```
Key: STRIPE_PUBLISHABLE_KEY
Value: pk_live_your_stripe_publishable_key_here
```

```
Key: STRIPE_SECRET_KEY
Value: sk_live_your_stripe_secret_key_here
```

For webhook secret, create a webhook endpoint first:
1. Go to [Stripe Webhooks](https://dashboard.stripe.com/webhooks)
2. Click **"Add endpoint"**
3. URL: `https://your-railway-app.up.railway.app/api/stripe/webhook/`
4. Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`
5. Copy the **Signing secret**

```
Key: STRIPE_WEBHOOK_SECRET
Value: whsec_your_webhook_signing_secret_here
```

## 📧 **Email Configuration (Brevo SMTP)**

Get credentials from [Brevo SMTP Settings](https://app.brevo.com/settings/keys/smtp):

```
Key: EMAIL_BACKEND
Value: django.core.mail.backends.smtp.EmailBackend
```

```
Key: EMAIL_HOST_USER
Value: your-brevo-email@example.com
```

```
Key: EMAIL_HOST_PASSWORD
Value: your-brevo-smtp-password
```

```
Key: DEFAULT_FROM_EMAIL
Value: ENTstore <awuleynovember@gmail.com>
```

```
Key: ADMIN_EMAIL
Value: Enontinoclothing@gmail.com
```

## 🌐 **Frontend Integration**

```
Key: FRONTEND_URL
Value: https://your-frontend-domain.vercel.app
```

## 🔐 **Generate Django Secret Key**

Use this Python command to generate a secure secret key:

```python
python -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits + '!@#$%^&*(-_=+)') for i in range(50)))"
```

Or use an online generator: https://djecrety.ir/

## 📋 **Complete Variables List**

Here's the complete list to copy-paste:

| Variable Name | Value | Required |
|---------------|-------|----------|
| `DJANGO_SECRET_KEY` | [50-char random string] | ✅ Yes |
| `DEBUG` | `False` | ✅ Yes |
| `RAILWAY_ENVIRONMENT` | `production` | ✅ Yes |
| `USE_SQLITE` | `False` | ✅ Yes |
| `STRIPE_PUBLISHABLE_KEY` | `pk_live_...` | ✅ Yes |
| `STRIPE_SECRET_KEY` | `sk_live_...` | ✅ Yes |
| `STRIPE_WEBHOOK_SECRET` | `whsec_...` | ✅ Yes |
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` | ✅ Yes |
| `EMAIL_HOST_USER` | Your Brevo email | ✅ Yes |
| `EMAIL_HOST_PASSWORD` | Your Brevo password | ✅ Yes |
| `DEFAULT_FROM_EMAIL` | `ENTstore <awuleynovember@gmail.com>` | ✅ Yes |
| `ADMIN_EMAIL` | `Enontinoclothing@gmail.com` | ✅ Yes |
| `FRONTEND_URL` | Your Vercel domain | ✅ Yes |

## 🚀 **After Adding Variables**

### **Step 3: Redeploy**
1. After adding all variables, Railway will automatically redeploy
2. Or manually trigger: **Settings** → **Redeploy**

### **Step 4: Verify Setup**
1. Check **Deployments** tab for successful deployment
2. View **Logs** for any errors
3. Test your API: `https://your-app.up.railway.app/api/products/`

## 🧪 **Test Your Configuration**

### **Test API Endpoints**
```bash
# Test products API
curl https://your-app.up.railway.app/api/products/

# Test admin access
curl https://your-app.up.railway.app/admin/

# Test Stripe webhook endpoint
curl -X POST https://your-app.up.railway.app/api/stripe/webhook/
```

### **Test Email Configuration**
1. Go to Django admin: `/admin/`
2. Create a test order
3. Check if email notifications are sent

### **Test Stripe Integration**
1. Use your frontend to make a test purchase
2. Check Stripe dashboard for payment events
3. Verify webhook events are received

## 🔍 **Troubleshooting**

### **Common Issues**

**Secret Key Error:**
```
ImproperlyConfigured: The SECRET_KEY setting must not be empty
```
**Solution:** Add `DJANGO_SECRET_KEY` variable

**Database Error:**
```
django.db.utils.OperationalError: could not connect to server
```
**Solution:** Ensure PostgreSQL service is running in Railway

**Stripe Error:**
```
stripe.error.AuthenticationError: No API key provided
```
**Solution:** Add `STRIPE_SECRET_KEY` variable

**Email Error:**
```
SMTPAuthenticationError: Username and Password not accepted
```
**Solution:** Verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`

**CORS Error:**
```
Access to fetch blocked by CORS policy
```
**Solution:** Add correct `FRONTEND_URL`

### **Check Logs**
1. Go to Railway dashboard
2. Select your service
3. Click **Logs** tab
4. Look for error messages

## 📞 **Need Help?**

1. **Railway Logs:** Check the Logs tab in Railway dashboard
2. **Django Admin:** Access `/admin/` to test functionality
3. **API Testing:** Use Postman or curl to test endpoints
4. **Stripe Dashboard:** Check for webhook events and payments

---

**Once all variables are added, your Railway backend will be fully configured for production! 🎉**