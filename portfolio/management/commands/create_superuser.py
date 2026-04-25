from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
import os

class Command(BaseCommand):
    help = 'Create or update the default superuser'

    def handle(self, *args, **options):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@saurabh.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        
        if not password:
            self.stdout.write(
                self.style.ERROR('DJANGO_SUPERUSER_PASSWORD environment variable not set')
            )
            return
            
        with transaction.atomic():
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email},
            )

            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(password)
            user.save()

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created superuser: {username}')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated superuser credentials: {username}')
                )
