from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Folders
from permissions import models, choices

@receiver(post_save, sender=Folders)
def create_permission(sender, instance, created, **kwargs):
  if created:
    models.Permission.objects.create(
      user=instance.created_by, type=choices.PermissionType.CREATOR, data=instance
    )