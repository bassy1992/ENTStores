from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Test admin login functionality'

    def handle(self, *args, **options):
        # Test user authentication
        try:
            user = User.objects.get(username='enontino')
            self.stdout.write(f"✅ User found: {user.username}")
            self.stdout.write(f"   Email: {user.email}")
            self.stdout.write(f"   Active: {user.is_active}")
            self.stdout.write(f"   Staff: {user.is_staff}")
            self.stdout.write(f"   Superuser: {user.is_superuser}")
            
            # Test authentication
            from django.contrib.auth import authenticate
            auth_user = authenticate(username='enontino', password='admin123456')
            if auth_user:
                self.stdout.write("✅ Authentication successful")
            else:
                self.stdout.write("❌ Authentication failed")
                return
            
            # Test admin access with test client
            client = Client()
            
            # Get login page
            response = client.get('/admin/login/')
            self.stdout.write(f"✅ Admin login page status: {response.status_code}")
            
            # Attempt login
            login_response = client.post('/admin/login/', {
                'username': 'enontino',
                'password': 'admin123456',
                'next': '/admin/'
            }, follow=True)
            
            self.stdout.write(f"✅ Login response status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                if 'Welcome' in login_response.content.decode() or 'Site administration' in login_response.content.decode():
                    self.stdout.write("✅ Admin login successful!")
                else:
                    self.stdout.write("❌ Login failed - check response content")
                    self.stdout.write(f"Response content preview: {login_response.content.decode()[:200]}")
            
        except User.DoesNotExist:
            self.stdout.write("❌ User 'enontino' not found")
        except Exception as e:
            self.stdout.write(f"❌ Error: {e}")