#!/usr/bin/env python3
"""
Production Terminal Setup
Configure your terminal environment to work directly with Railway production database
"""

import os
import sys
import subprocess
import json


def create_production_env_file():
    """Create a .env.production file for production database access"""
    env_content = '''# Production Environment Configuration
# Copy your Railway DATABASE_URL here for direct production access

# Railway Database URL (get this from Railway dashboard)
DATABASE_URL=postgresql://postgres:password@host:port/database

# Production Settings
DJANGO_SETTINGS_MODULE=myproject.settings
RAILWAY_ENVIRONMENT=production
DEBUG=False

# Optional: Railway API Token for CLI access
RAILWAY_TOKEN=your_railway_token_here

# Usage Instructions:
# 1. Replace DATABASE_URL with your actual Railway database URL
# 2. Get DATABASE_URL from Railway dashboard > Variables
# 3. Load this file: source .env.production (Linux/Mac) or set variables manually (Windows)
# 4. Run Django commands: python backend/manage.py <command>
'''
    
    with open('.env.production', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env.production file")
    print("   Edit this file with your Railway database credentials")


def create_production_scripts():
    """Create helper scripts for production database access"""
    
    # Django management script
    django_script = '''#!/usr/bin/env python3
"""
Production Django Management Script
Run Django commands against production database
"""

import os
import sys
import django

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
os.environ.setdefault('RAILWAY_ENVIRONMENT', 'production')

# Setup Django
django.setup()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    
    # Add 'manage.py' as first argument if not present
    if len(sys.argv) == 1 or sys.argv[1] != 'manage.py':
        sys.argv.insert(1, 'manage.py')
    
    execute_from_command_line(sys.argv[1:])
'''
    
    with open('prod_manage.py', 'w') as f:
        f.write(django_script)
    
    # Database shell script
    db_shell_script = '''#!/usr/bin/env python3
"""
Production Database Shell
Direct access to production PostgreSQL database
"""

import os
import sys
import django

# Setup
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
os.environ.setdefault('RAILWAY_ENVIRONMENT', 'production')

django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    print("🗄️  Opening production database shell...")
    print("   Type \\q to quit")
    call_command('dbshell')
'''
    
    with open('prod_dbshell.py', 'w') as f:
        f.write(db_shell_script)
    
    # Django shell script
    django_shell_script = '''#!/usr/bin/env python3
"""
Production Django Shell
Interactive Python shell with production database access
"""

import os
import sys
import django

# Setup
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
os.environ.setdefault('RAILWAY_ENVIRONMENT', 'production')

django.setup()

# Import common models for convenience
from shop.models import *
from django.contrib.auth.models import User

if __name__ == '__main__':
    print("🐍 Opening production Django shell...")
    print("   Available models: Product, Category, Order, OrderItem, etc.")
    print("   Example: Product.objects.all()")
    
    from django.core.management import call_command
    call_command('shell')
'''
    
    with open('prod_shell.py', 'w') as f:
        f.write(django_shell_script)
    
    print("✅ Created production scripts:")
    print("   - prod_manage.py (Django management)")
    print("   - prod_dbshell.py (Database shell)")
    print("   - prod_shell.py (Django shell)")


def create_production_commands():
    """Create batch/shell files for easy command execution"""
    
    # Windows batch files
    if os.name == 'nt':
        # Production manage command
        with open('prod.bat', 'w') as f:
            f.write('@echo off\npython prod_manage.py %*\n')
        
        # Database shell
        with open('proddb.bat', 'w') as f:
            f.write('@echo off\npython prod_dbshell.py\n')
        
        # Django shell
        with open('prodshell.bat', 'w') as f:
            f.write('@echo off\npython prod_shell.py\n')
        
        print("✅ Created Windows batch files:")
        print("   - prod.bat <command> (e.g., prod.bat migrate)")
        print("   - proddb.bat (database shell)")
        print("   - prodshell.bat (Django shell)")
    
    else:
        # Unix shell scripts
        scripts = {
            'prod': 'python3 prod_manage.py "$@"',
            'proddb': 'python3 prod_dbshell.py',
            'prodshell': 'python3 prod_shell.py'
        }
        
        for name, command in scripts.items():
            with open(name, 'w') as f:
                f.write(f'#!/bin/bash\n{command}\n')
            os.chmod(name, 0o755)
        
        print("✅ Created Unix shell scripts:")
        print("   - ./prod <command> (e.g., ./prod migrate)")
        print("   - ./proddb (database shell)")
        print("   - ./prodshell (Django shell)")


def create_production_utilities():
    """Create utility scripts for common production tasks"""
    
    utils_script = '''#!/usr/bin/env python3
"""
Production Database Utilities
Common tasks for production database management
"""

import os
import sys
import django

# Setup
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
os.environ.setdefault('RAILWAY_ENVIRONMENT', 'production')

django.setup()

from shop.models import Product, Category, Order, OrderItem
from django.contrib.auth.models import User


def show_stats():
    """Show production database statistics"""
    print("📊 Production Database Statistics")
    print("=" * 35)
    print(f"Products: {Product.objects.count()}")
    print(f"Categories: {Category.objects.count()}")
    print(f"Orders: {Order.objects.count()}")
    print(f"Users: {User.objects.count()}")
    
    # Products with URL images
    url_products = Product.objects.filter(image_url__isnull=False).exclude(image_url='')
    print(f"Products with URL images: {url_products.count()}")
    
    # Featured products
    featured = Product.objects.filter(is_featured=True)
    print(f"Featured products: {featured.count()}")


def list_products():
    """List all products"""
    print("📦 Production Products")
    print("=" * 25)
    
    products = Product.objects.all()[:20]  # First 20
    for product in products:
        image_type = "URL" if product.image_url else "File" if product.image else "None"
        status = "✓" if product.is_active else "✗"
        print(f"{status} {product.id}: {product.title} (${product.price}) [{image_type}]")
    
    if Product.objects.count() > 20:
        print(f"... and {Product.objects.count() - 20} more products")


def list_orders():
    """List recent orders"""
    print("🛒 Recent Orders")
    print("=" * 15)
    
    orders = Order.objects.all()[:10]  # Last 10
    for order in orders:
        print(f"{order.id}: {order.customer_name} - ${order.total} ({order.status})")


def backup_data():
    """Create a data backup"""
    print("💾 Creating data backup...")
    
    from django.core.management import call_command
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"production_backup_{timestamp}.json"
    
    try:
        call_command('dumpdata', '--natural-foreign', '--natural-primary', 
                    '--exclude=contenttypes', '--exclude=auth.permission',
                    '--output='+filename)
        print(f"✅ Backup created: {filename}")
    except Exception as e:
        print(f"❌ Backup failed: {e}")


def main():
    """Main utility function"""
    if len(sys.argv) < 2:
        print("🛠️  Production Database Utilities")
        print("=" * 35)
        print("Usage: python prod_utils.py <command>")
        print("")
        print("Commands:")
        print("  stats     - Show database statistics")
        print("  products  - List products")
        print("  orders    - List recent orders")
        print("  backup    - Create data backup")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'stats':
        show_stats()
    elif command == 'products':
        list_products()
    elif command == 'orders':
        list_orders()
    elif command == 'backup':
        backup_data()
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == '__main__':
    main()
'''
    
    with open('prod_utils.py', 'w') as f:
        f.write(utils_script)
    
    print("✅ Created prod_utils.py")
    print("   Usage: python prod_utils.py <stats|products|orders|backup>")


def create_railway_cli_setup():
    """Create Railway CLI setup instructions"""
    
    railway_setup = '''# Railway CLI Setup for Direct Production Access

## Install Railway CLI

### Windows (PowerShell)
```powershell
iwr -useb https://railway.app/install.ps1 | iex
```

### macOS/Linux
```bash
curl -fsSL https://railway.app/install.sh | sh
```

## Login and Setup
```bash
# Login to Railway
railway login

# Link to your project (run in project directory)
railway link

# Get environment variables
railway variables

# Connect to production database directly
railway connect postgres
```

## Useful Railway Commands
```bash
# View logs
railway logs

# Open project dashboard
railway open

# Run commands in production environment
railway run python manage.py migrate
railway run python manage.py shell

# Get database URL
railway variables get DATABASE_URL
```

## Environment Variables Setup
1. Get your DATABASE_URL: `railway variables get DATABASE_URL`
2. Copy it to your .env.production file
3. Use the production scripts to work with the database

## Direct Database Access
```bash
# Using Railway CLI
railway connect postgres

# Using local scripts (after setting up .env.production)
python prod_dbshell.py
```
'''
    
    with open('RAILWAY_CLI_SETUP.md', 'w') as f:
        f.write(railway_setup)
    
    print("✅ Created RAILWAY_CLI_SETUP.md")


def main():
    """Main setup function"""
    print("🚀 Production Terminal Setup")
    print("=" * 30)
    
    print("\n1. Creating environment configuration...")
    create_production_env_file()
    
    print("\n2. Creating production scripts...")
    create_production_scripts()
    
    print("\n3. Creating command shortcuts...")
    create_production_commands()
    
    print("\n4. Creating utility scripts...")
    create_production_utilities()
    
    print("\n5. Creating Railway CLI setup guide...")
    create_railway_cli_setup()
    
    print("\n🎉 Production Terminal Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Edit .env.production with your Railway DATABASE_URL")
    print("2. Install Railway CLI (see RAILWAY_CLI_SETUP.md)")
    print("3. Use the created scripts for production access:")
    
    if os.name == 'nt':
        print("   - prod.bat migrate (run migrations)")
        print("   - prodshell.bat (Django shell)")
        print("   - proddb.bat (database shell)")
    else:
        print("   - ./prod migrate (run migrations)")
        print("   - ./prodshell (Django shell)")
        print("   - ./proddb (database shell)")
    
    print("   - python prod_utils.py stats (database stats)")
    
    print("\n🔗 Get your DATABASE_URL from:")
    print("   Railway Dashboard > Your Project > Variables > DATABASE_URL")


if __name__ == '__main__':
    main()