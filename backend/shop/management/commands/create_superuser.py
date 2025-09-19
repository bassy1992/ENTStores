from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a superuser for development'

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists'))
            return
        
        User.objects.create_superuser(
            username='admin',
            email='admin@ennc.com',
            password='admin123'
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created superuser "admin" with password "admin123"')
        )