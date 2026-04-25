from django.core.management.base import BaseCommand
from portfolio.superuser import ensure_default_superuser

class Command(BaseCommand):
    help = 'Create or update the default superuser'

    def handle(self, *args, **options):
        success, message = ensure_default_superuser()
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))
