#!/usr/bin/env python
"""
Fix production admin issues by running migrations and checking database integrity
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Set up Django environment for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Force production environment
os.environ['DEBUG'] = 'false'
os.environ['RENDER'] = 'true'

def main():
    """Run production fixes"""
    print("🔧 Fixing Production Admin Issues")
    print("=" * 50)
    
    try:
        # Initialize Django
        django.setup()
        
        print("1. Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        
        print("\n2. Checking migration status...")
        execute_from_command_line(['manage.py', 'showmigrations'])
        
        print("\n3. Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("\n✅ Production fixes completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during production fixes: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()