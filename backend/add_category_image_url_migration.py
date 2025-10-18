#!/usr/bin/env python3
"""
Script to create and apply migration for adding image_url field to Category model
"""

import os
import sys
import django
import subprocess

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()


def create_migration():
    """Create migration for the new image_url field"""
    print("🔄 Creating migration for Category image_url field...")
    
    try:
        # Change to backend directory
        os.chdir('backend')
        
        # Create migration
        result = subprocess.run([
            sys.executable, 'manage.py', 'makemigrations', 'shop',
            '--name', 'add_category_image_url'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migration created successfully")
            print(result.stdout)
        else:
            print("❌ Error creating migration:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True


def apply_migration():
    """Apply the migration"""
    print("🔄 Applying migration...")
    
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Migration applied successfully")
            print(result.stdout)
        else:
            print("❌ Error applying migration:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True


def main():
    """Main function"""
    print("🗄️  Category Image URL Migration")
    print("=" * 40)
    
    if create_migration():
        if apply_migration():
            print("\n✅ Category model updated successfully!")
            print("   Categories can now use image URLs instead of file uploads")
        else:
            print("\n❌ Migration created but failed to apply")
    else:
        print("\n❌ Failed to create migration")


if __name__ == '__main__':
    main()