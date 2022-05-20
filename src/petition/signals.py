from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from account.models import User
from petition.models import Notification, Petition, Vote


@receiver(post_save, sender=Vote)
def increase_signatories_count(sender, instance: Vote, created: bool = False, **kwargs):
    if not created:
        return

    instance.petition.signatories_count += 1
    instance.petition.save(update_fields=("signatories_count",))


@receiver(post_delete, sender=Vote)
def increase_signatories_count(sender, instance: Vote, created: bool = False, **kwargs):
    if not created:
        return

    petition = instance.petition
    petition.signatories_count = max(1, petition.signatories_count - 1)
    petition.save(update_fields=("signatories_count",))
