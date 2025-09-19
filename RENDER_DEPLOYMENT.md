# Render Deployment Guide

## Overview
Deploy your ENTstore application to Render with PostgreSQL database.

## Prerequisites
1. Render account (render.com)
2. GitHub repository connected to Render

## Deployment Options

### Option 1: Using render.yaml (Recommended)
The `render.yaml` file in the root directory contains the complete configuration.

1. **Connect Repository to Render**
   - Go to render.com dashboard
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

2. **Set Environment Variables**
   After deployment, set these environment variables in Render dashboard:

   **Backend Service:**
   ```
   STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key_here
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_here
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
   EMAIL_HOST_USER=your_email@smtp-brevo.com
   EMAIL_HOST_PASSWORD=your_email_password_here
   ```

   **Frontend Service:**
   ```
   VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key_here
   ```

### Option 2: Manual Setup

#### Backend Setup
1. **Create Web Service**
   - Service Type: Web Service
   - Environment: Python 3
   - Build Command: `./build.sh`
   - Start Command: `cd backend && gunicorn myproject.wsgi:application`

2. **Create PostgreSQL Database**
   - Go to Dashboard → New → PostgreSQL
   - Note the connection details

3. **Environment Variables**
   Set the same variables as listed in Option 1.

#### Frontend Setup
1. **Create Static Site**
   - Service Type: Static Site
   - Build Command: `cd frontend && npm ci && npm run build`
   - Publish Directory: `frontend/dist`

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