#!/usr/bin/env python
"""
Production deployment script to fix admin issues
This script should be run on the production server (Render)
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_production_environment():
    """Set up production environment variables"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    
    # Force production settings
    os.environ['DEBUG'] = 'false'
    os.environ['RENDER'] = 'true'
    
    # Ensure we're using PostgreSQL in production
    if not os.getenv('DATABASE_URL'):
        print("❌ DATABASE_URL not found. This script must run on production.")
        sys.exit(1)

def main():
    """Main deployment function"""
    print("🚀 Production Admin Fix Deployment")
    print("=" * 50)
    
    setup_production_environment()
    
    try:
        # Initialize Django
        django.setup()
        
        print("1. 📋 Checking current migration status...")
        execute_from_command_line(['manage.py', 'showmigrations', 'shop'])
        
        print("\n2. 🔄 Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        
        print("\n3. 🧪 Testing admin functionality...")
        execute_from_command_line(['manage.py', 'fix_admin'])
        
        print("\n4. 📦 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--verbosity=1'])
        
        print("\n✅ Production deployment completed successfully!")
        print("🌐 Admin should now be accessible at: https://entstores.onrender.com/admin/shop/orderitem/")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()