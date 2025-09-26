# 🔑 Stripe Live Keys - Setup Checklist

## ✅ Keys Added to Configuration

### Live Keys Configured:
- **Publishable Key**: `pk_live_51RHlGq...` (configured in .env.production)
- **Secret Key**: `sk_live_51RHlGq...` (configured in .env.production)

## 🚀 Deployment Steps

### 1. Set Environment Variables in Render (Backend)
Go to your Render dashboard > Backend service > Environment:

```
STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_ACTUAL_LIVE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY=sk_live_YOUR_ACTUAL_LIVE_SECRET_KEY
```

### 2. Set Environment Variables in Vercel (Frontend)
Go to your Vercel dashboard > Project > Settings > Environment Variables:

```
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_YOUR_ACTUAL_LIVE_PUBLISHABLE_KEY
```

### 3. Set Up Live Webhook in Stripe
1. Go to [Stripe Dashboard](https://dashboard.stripe.com) (Live mode)
2. Go to **Developers > Webhooks**
3. Click **Add endpoint**
4. **Endpoint URL**: `https://entstores.onrender.com/api/payments/stripe/webhook/`
5. **Events**:
   - `checkout.session.completed`
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
6. Copy the **Signing secret** (starts with `whsec_`)
7. Add to Render environment: `STRIPE_WEBHOOK_SECRET=whsec_...`

## ⚠️ Important Security Notes

- ✅ Live keys are now in production config only
- ✅ Test keys remain in development config
- ⚠️ **Never commit live keys to Git**
- ⚠️ **Test thoroughly before going live**

## 🧪 Testing Checklist

### Before Going Live:
- [ ] Environment variables set in Render
- [ ] Environment variables set in Vercel
- [ ] Live webhook configured and working
- [ ] Test payment with real card (small amount)
- [ ] Verify payment appears in Stripe Dashboard
- [ ] Test order confirmation emails
- [ ] Test failed payment handling

## 🎉 Ready to Accept Live Payments!

Once all steps are complete, your store will accept real payments through Stripe.

**Remember**: Always test with small amounts first!