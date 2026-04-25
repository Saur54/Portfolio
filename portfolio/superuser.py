from django.contrib.auth import get_user_model
from django.db import transaction

DEFAULT_SUPERUSER_USERNAME = 'saurabh'
DEFAULT_SUPERUSER_EMAIL = 'saurabh74776@gmail.com'
DEFAULT_SUPERUSER_PASSWORD = 'Saurabh126##'


def ensure_default_superuser():
    """
    Create or update the default admin user from environment variables.

    Returns:
        tuple[bool, str]: (success, message)
    """
    username = DEFAULT_SUPERUSER_USERNAME
    email = DEFAULT_SUPERUSER_EMAIL
    password = DEFAULT_SUPERUSER_PASSWORD

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
