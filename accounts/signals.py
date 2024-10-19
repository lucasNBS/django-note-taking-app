from django.db.models.signals import post_save
from django.dispatch import receiver

from folders.models import Folders
from permissions import choices, models

from .models import User


@receiver(post_save, sender=User)
def create_permission(sender, instance, created, **kwargs):
    if created:
        models.Permission.objects.create(
            user=instance, type=choices.PermissionType.READER, data=Folders.get_default_id()
        )
