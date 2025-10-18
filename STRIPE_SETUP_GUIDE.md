# 🔑 Stripe Production Keys Setup Guide

## Current Status
- ✅ **Development**: Using test keys (correct)
- ❌ **Production**: Using test keys (needs live keys)

## Step 1: Get Live Stripe Keys

### 1.1 Access Stripe Dashboard
1. Go to [https://dashboard.stripe.com](https://dashboard.stripe.com)
2. **Switch to Live mode** (toggle in top-left corner)
3. Make sure you see "Live" indicator

### 1.2 Get API Keys
1. Go to **Developers > API keys**
2. Copy **Publishable key** (starts with `pk_live_`)
3. Reveal and copy **Secret key** (starts with `sk_live_`)

### 1.3 Set up Live Webhook
1. Go to **Developers > Webhooks**
2. Click **Add endpoint**
3. **Endpoint URL**: `https://entstores-production.up.railway.app/api/payments/stripe/webhook/`
4. **Events to send**:
   - `checkout.session.completed`
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
5. Click **Add endpoint**
6. Copy the **Signing secret** (starts with `whsec_`)

## Step 2: Update Environment Variables

### 2.1 Update .env.production file
Replace the placeholder values in `.env.production`:

```bash
# Stripe Payment Settings (LIVE KEYS FOR PRODUCTION)
STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_ACTUAL_LIVE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY=sk_live_YOUR_ACTUAL_LIVE_SECRET_KEY
STRIPE_WEBHOOK_SECRET=whsec_YOUR_ACTUAL_LIVE_WEBHOOK_SECRET
STRIPE_ENDPOINT_SECRET=whsec_YOUR_ACTUAL_LIVE_WEBHOOK_SECRET
STRIPE_API_VERSION=2023-10-16
```

### 2.2 Set Environment Variables in Railway
1. Go to your **Railway Dashboard**
2. Select your **backend service**
3. Go to **Environment** tab
4. Add/Update these variables:
   - `STRIPE_PUBLISHABLE_KEY` = `pk_live_...`
   - `STRIPE_SECRET_KEY` = `sk_live_...`
   - `STRIPE_WEBHOOK_SECRET` = `whsec_...`
   - `STRIPE_ENDPOINT_SECRET` = `whsec_...`

### 2.3 Set Frontend Environment Variable
1. Go to your **Vercel Dashboard** (or frontend hosting)
2. Go to **Settings > Environment Variables**
3. Add:
   - `VITE_STRIPE_PUBLISHABLE_KEY` = `pk_live_...`

## Step 3: Test the Setup

### 3.1 Test Webhook
1. In Stripe Dashboard > Webhooks
2. Click on your webhook endpoint
3. Click **Send test webhook**
4. Verify it reaches your backend successfully

### 3.2 Test Payment Flow
1. Place a test order on your live site
2. Use a real credit card (will be charged)
3. Verify the payment completes successfully
4. Check Stripe Dashboard for the payment

## Step 4: Security Checklist

### ✅ Security Best Practices
- [ ] Live keys are only in production environment
- [ ] Test keys are only in development environment
- [ ] Webhook endpoint is secured with signature verification
- [ ] API keys are not exposed in frontend code
- [ ] Environment variables are properly set in hosting platforms

### ⚠️ Important Notes
- **Never commit live keys to Git**
- **Test thoroughly before going live**
- **Monitor Stripe Dashboard for failed payments**
- **Set up proper error handling for failed payments**

## Step 5: Go Live Checklist

### Before Accepting Live Payments:
- [ ] Stripe account is fully verified
- [ ] Business information is complete in Stripe
- [ ] Tax settings are configured
- [ ] Payout schedule is set up
- [ ] Live webhook is working
- [ ] Test payments work end-to-end
- [ ] Error handling is implemented
- [ ] Customer email receipts are working

## Troubleshooting

### Common Issues:
1. **"Invalid API key"** - Check key format and Live/Test mode
2. **"Webhook signature verification failed"** - Verify webhook secret
3. **"Payment not completing"** - Check webhook endpoint accessibility
4. **"Frontend shows test mode"** - Update VITE_STRIPE_PUBLISHABLE_KEY

### Support:
- Stripe Documentation: https://stripe.com/docs
- Stripe Support: https://support.stripe.com