#!/bin/bash

# Complete Deployment Script for Backend + Frontend

echo "🚀 Starting complete deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."
    
    if ! command -v railway &> /dev/null; then
        print_warning "Railway CLI not found. Installing..."
        npm install -g @railway/cli
    fi
    
    if ! command -v vercel &> /dev/null; then
        print_warning "Vercel CLI not found. Installing..."
        npm install -g vercel
    fi
}

# Deploy backend to Railway
deploy_backend() {
    print_status "Deploying backend to Railway..."
    
    cd backend
    
    # Check if logged in to Railway
    if ! railway whoami &> /dev/null; then
        print_warning "Please login to Railway..."
        railway login
    fi
    
    # Deploy
    print_status "Deploying to Railway..."
    railway up
    
    if [ $? -eq 0 ]; then
        print_status "Backend deployed successfully!"
        
        # Get the Railway URL
        RAILWAY_URL=$(railway status --json | grep -o '"url":"[^"]*' | cut -d'"' -f4)
        if [ ! -z "$RAILWAY_URL" ]; then
            print_status "Backend URL: $RAILWAY_URL"
            echo "$RAILWAY_URL" > ../backend_url.txt
        fi
    else
        print_error "Backend deployment failed!"
        exit 1
    fi
    
    cd ..
}

# Deploy frontend to Vercel
deploy_frontend() {
    print_status "Deploying frontend to Vercel..."
    
    cd frontend
    
    # Check if logged in to Vercel
    if ! vercel whoami &> /dev/null; then
        print_warning "Please login to Vercel..."
        vercel login
    fi
    
    # Set environment variables if backend URL is available
    if [ -f "../backend_url.txt" ]; then
        BACKEND_URL=$(cat ../backend_url.txt)
        print_status "Setting VITE_API_URL to: $BACKEND_URL"
        vercel env add VITE_API_URL production <<< "$BACKEND_URL"
    fi
    
    # Deploy
    print_status "Deploying to Vercel..."
    vercel --prod
    
    if [ $? -eq 0 ]; then
        print_status "Frontend deployed successfully!"
    else
        print_error "Frontend deployment failed!"
        exit 1
    fi
    
    cd ..
}

# Main deployment process
main() {
    print_status "Starting complete deployment process..."
    
    check_dependencies
    deploy_backend
    deploy_frontend
    
    print_status "✅ Deployment complete!"
    print_status "Next steps:"
    echo "1. Set environment variables in Railway dashboard"
    echo "2. Set environment variables in Vercel dashboard"
    echo "3. Test your application"
    echo "4. Update CORS settings if needed"
    
    # Clean up
    rm -f backend_url.txt
}

# Run main function
main