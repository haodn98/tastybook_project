import logging
from django.dispatch import receiver
from djoser.signals import user_registered, user_activated, user_updated

logger = logging.getLogger('user_activity')


@receiver(user_registered)
def log_user_registered(sender, user, request, **kwargs):
    logger.info(f'User registered: {user.email} - {user.id}')


@receiver(user_activated)
def log_user_activated(sender, user, request, **kwargs):
    logger.info(f'User activated: {user.email} - {user.id}')


@receiver(user_updated)
def log_user_updated(sender, user, request, **kwargs):
    logger.info(f'User password reset: {user.email} - {user.id}')
