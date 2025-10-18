# ⚠️ DEPRECATED - Render Deployment Guide (Use Railway Instead)

## Overview
⚠️ **DEPRECATED**: This project now uses Railway for deployment. See RAILWAY_DASHBOARD_SETUP.md instead.

Deploy your ENTstore Django backend to Render with PostgreSQL database.

## Prerequisites
1. Render account (render.com)
2. GitHub repository connected to Render

## Manual Deployment Steps

### Step 1: Create PostgreSQL Database
1. Go to Render Dashboard → "New" → "PostgreSQL"
2. Name: `entstore-db`
3. Database Name: `entstore`
4. User: `entstore_user`
5. Plan: Free
6. Click "Create Database"
7. **Save the DATABASE_URL** from the database info page

### Step 2: Deploy Backend
1. **Create Web Service**
   - Go to Dashboard → "New" → "Web Service"
   - Connect your GitHub repository
   - Name: `entstore-backend`
   - Environment: `Python 3`
   - Build Command: `./build.sh`
   - Start Command: `cd backend && gunicorn myproject.wsgi:application --host 0.0.0.0 --port $PORT`

2. **Set Environment Variables**
   In the service settings, add these environment variables:
   ```
   DEBUG=false
   DJANGO_SECRET_KEY=your_generated_secret_key_here
   DATABASE_URL=postgresql://... (from Step 1)
   STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
   EMAIL_HOST_USER=your_email_user@smtp-brevo.com
   EMAIL_HOST_PASSWORD=your_email_password_here
   ```

3. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy from your GitHub repository

## Post-Deployment Steps

1. **Create Superuser**
   ```bash
   # In Render shell for backend service
   python manage.py createsuperuser
   ```

2. **Test the Application**
   - Backend: `https://your-backend.onrender.com`
   - Frontend: `https://your-frontend.onrender.com`

3. **Update CORS Settings**
   The `render.yaml` automatically configures the frontend URL for CORS.

## Environment Variables Reference

### Backend Required Variables
- `DEBUG=false`
- `DJANGO_SECRET_KEY` (auto-generated)
- `DATABASE_URL` (auto-provided by PostgreSQL service)
- `FRONTEND_URL` (set to frontend service URL)

### Payment Variables
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`

### Email Variables
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

### Frontend Variables
- `VITE_API_URL` (set to backend service URL)
- `VITE_STRIPE_PUBLISHABLE_KEY`

## Troubleshooting

### Common Issues
1. **Build Failures**: Check build logs in Render dashboard
2. **Database Connection**: Ensure DATABASE_URL is properly set
3. **CORS Errors**: Verify FRONTEND_URL is set correctly
4. **Static Files**: Ensure collectstatic runs in build process

### Useful Commands
```bash
# Check logs
# Available in Render dashboard under "Logs"

# Access shell (available in Render dashboard)
python manage.py shell

# Run migrations manually
python manage.py migrate
```

## Free Tier Limitations
- Services sleep after 15 minutes of inactivity
- 750 hours per month per service
- Database connections may be limited

## Scaling
- Upgrade to paid plans for:
  - Always-on services
  - More resources
  - Custom domains
  - SSL certificates