import logging

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .superuser import ensure_default_superuser

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def bootstrap_default_superuser(sender, **kwargs):
    """
    Ensure the default admin user exists after migrations run.

    This acts as a safety net for deployments where a pre-deploy bootstrap
    command is not easy to run manually.
    """
    app_label = getattr(sender, 'label', None)
    if app_label != 'portfolio':
        return

    success, message = ensure_default_superuser()
    if success:
        logger.info(message)
    else:
        logger.warning(message)
