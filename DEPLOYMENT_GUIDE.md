# Complete Deployment Guide - Backend (Railway) + Frontend (Vercel)

## Overview
- **Backend**: Django REST API deployed on Railway with PostgreSQL database
- **Frontend**: React/Vite app deployed on Vercel
- **Database**: PostgreSQL on Railway

## Part 1: Deploy Backend to Railway

### Prerequisites
1. Railway account (railway.app)
2. Railway CLI: `npm install -g @railway/cli`

### Step 1: Deploy Backend
```bash
# Navigate to backend
cd backend

# Login to Railway
railway login

# Initialize or link project
railway init  # or railway link if project exists

# Deploy
railway up
```

### Step 2: Add PostgreSQL Database
1. Go to Railway dashboard
2. Click "New" → "Database" → "PostgreSQL"
3. Railway automatically provides `DATABASE_URL`

### Step 3: Set Environment Variables
In Railway dashboard, add these variables:

**Required:**
```
DEBUG=False
DJANGO_SECRET_KEY=your_generated_secret_key_here
DATABASE_URL=postgresql://... (auto-provided by Railway)
```

**Payment:**
```
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

**Email:**
```
EMAIL_HOST_USER=your_email_host_user@smtp-brevo.com
EMAIL_HOST_PASSWORD=your_email_host_password_here
```

**Frontend URL (update after frontend deployment):**
```
FRONTEND_URL=https://your-app.vercel.app
```

### Step 4: Run Initial Setup
```bash
# Create superuser
railway run python manage.py createsuperuser

# Check deployment
railway logs
```

Your backend will be available at: `https://your-app.up.railway.app`

## Part 2: Deploy Frontend to Vercel

### Prerequisites
1. Vercel account (vercel.com)
2. Vercel CLI: `npm install -g vercel`

### Step 1: Update API URLs
First, update your frontend to use environment variables for API URLs.

### Step 2: Deploy to Vercel
```bash
# Navigate to frontend
cd frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Step 3: Set Environment Variables in Vercel
In Vercel dashboard → Settings → Environment Variables:

```
VITE_API_URL=https://your-backend.up.railway.app
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
```

## Part 3: Update Cross-Origin Settings

### Update Backend CSRF Settings
After frontend deployment, update Railway environment variables:
```
FRONTEND_URL=https://your-app.vercel.app
```

### Update Frontend API Calls
Replace hardcoded localhost URLs with environment variable.

## Quick Deploy Commands

### Backend (Railway)
```bash
cd backend
railway login
railway up
```

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

## Post-Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] Database connected and migrated
- [ ] Frontend deployed and accessible
- [ ] API calls working between frontend and backend
- [ ] Payment system functional
- [ ] Email system working
- [ ] CORS configured properly
- [ ] SSL certificates active (automatic)

## Troubleshooting

### Backend Issues
```bash
railway logs                    # Check logs
railway run python manage.py shell  # Access Django shell
railway connect postgres       # Connect to database
```

### Frontend Issues
```bash
vercel logs                     # Check deployment logs
vercel dev                      # Test locally
```

## Domain Configuration (Optional)

### Custom Domain for Backend (Railway)
1. Railway dashboard → Settings → Domains
2. Add custom domain
3. Update DNS records

### Custom Domain for Frontend (Vercel)
1. Vercel dashboard → Settings → Domains
2. Add custom domain
3. Update DNS records