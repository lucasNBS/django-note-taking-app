from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Note

from folders.models import Folders
from permissions import models, choices

@receiver(post_save, sender=Note)
def create_permission_for_users_that_has_access(sender, instance, created, **kwargs):
  if created:
    folder = instance.folder

    # Do not share notes in General folder
    if folder.id == Folders.objects.filter(title="General").first().id:
      return

    permissions = models.Permission.objects.filter(data=folder).exclude(
      type=choices.PermissionType.CREATOR
    )

    for permission in permissions:
      models.Permission.objects.create(
        user=permission.user, type=permission.type, data=instance
      )