"""
Small helper to create or update a Django superuser non-interactively.
Usage:
  python create_superuser_script.py admin@example.com adminpassword admin
This will create a superuser with username 'admin' and email and password provided.
"""
import os
import sys

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python create_superuser_script.py <email> <password> <username>')
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    username = sys.argv[3]

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

    import django
    django.setup()

    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        user = User.objects.filter(email=email).first()
        if user:
            user.is_staff = True
            user.is_superuser = True
            user.username = username
            user.set_password(password)
            user.save()
            print(f'Updated existing user {email}')
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f'Created superuser {email}')
    except Exception as e:
        print('Error creating superuser:', e)
        sys.exit(2)
