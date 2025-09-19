# Railway Deployment Guide

## Prerequisites
1. Railway account (sign up at railway.app)
2. Railway CLI installed: `npm install -g @railway/cli`
3. PostgreSQL database already set up on Railway

## Deployment Steps

### 1. Login to Railway
```bash
railway login
```

### 2. Create or Link Project
```bash
# If creating new project
railway init

# If linking to existing project
railway link
```

### 3. Add PostgreSQL Database (if not already added)
- Go to your Railway dashboard
- Click "New" → "Database" → "PostgreSQL"
- Railway will automatically provide the DATABASE_URL

### 4. Set Environment Variables
Go to your Railway project dashboard and add these variables:

**Required Variables:**
- `DEBUG=False`
- `DJANGO_SECRET_KEY=your_secret_key_here`
- `DATABASE_URL=postgresql://...` (automatically provided by Railway PostgreSQL)

**Payment Variables:**
- `STRIPE_PUBLISHABLE_KEY=pk_test_...`
- `STRIPE_SECRET_KEY=sk_test_...`
- `STRIPE_WEBHOOK_SECRET=whsec_...`

**Email Variables:**
- `EMAIL_HOST_USER=81d61b003@smtp-brevo.com`
- `EMAIL_HOST_PASSWORD=your_brevo_password`

**Frontend URL:**
- `FRONTEND_URL=https://your-frontend-domain.vercel.app`

### 5. Deploy
```bash
railway up
```

### 6. Run Migrations (if needed)
```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
```

### 7. Create Superuser (optional)
```bash
railway run python manage.py createsuperuser
```

## Important Notes

1. **Database Connection**: Railway automatically provides DATABASE_URL when you add a PostgreSQL service
2. **Static Files**: WhiteNoise handles static files automatically
3. **CORS**: Update CSRF_TRUSTED_ORIGINS in settings.py with your Railway domain
4. **Domain**: Railway provides a domain like `your-app.up.railway.app`

## Troubleshooting

### Check Logs
```bash
railway logs
```

### Connect to Database
```bash
railway connect postgres
```

### Run Commands
```bash
railway run python manage.py shell
```

## Post-Deployment

1. Update your frontend API URLs to point to your Railway backend
2. Test all endpoints
3. Update CORS settings if needed
4. Set up custom domain (optional)