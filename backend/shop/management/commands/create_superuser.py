from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create a superuser for production deployment'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Username for superuser')
        parser.add_argument('--email', type=str, default='admin@entstore.com', help='Email for superuser')
        parser.add_argument('--password', type=str, help='Password for superuser')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password'] or os.environ.get('ADMIN_PASSWORD', 'entstore2024!')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists'))
            return
        
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created superuser "{username}" with email "{email}"')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Password: {password}')
        )