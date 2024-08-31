from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from permissions import models, choices
from folders.models import Folders

@receiver(post_save, sender=User)
def create_permission(sender, instance, created, **kwargs):
  if created:
    models.Permission.objects.create(
      user=instance, type=choices.PermissionType.READER, data=Folders.objects.get(pk=1)
    )