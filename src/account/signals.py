from petition.models import Notification

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


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
