import os

from django.contrib.auth import get_user_model
from django.db import transaction


def ensure_default_superuser():
    """
    Create or update the default admin user from environment variables.

    Returns:
        tuple[bool, str]: (success, message)
    """
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@saurabh.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    if not password:
        return False, 'DJANGO_SUPERUSER_PASSWORD environment variable not set'

    User = get_user_model()

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
        return True, f'Successfully created superuser: {username}'

    return True, f'Successfully updated superuser credentials: {username}'
