from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from petition.models import Notification

from .models import User


@receiver(pre_delete, sender=User)
def prohibit_superuser_deletion(sender, instance: User, **kwargs):
    if instance.is_superuser:
        raise PermissionDenied


@receiver(post_save, sender=User)
def send_welcome_notification(sender, instance: User, created: bool = False, **kwargs):
    if not created:
        return

    Notification.objects.create(
        user=instance,
        title="Welcome to the Une Pétition!",
        description="You can start by creating a new petition, "
        "or supporting someone else's.",
    )
