from django.db import models
from accounts.models import User
from core.models import ShareableModel
from core.choices import DataType
from .choices import PermissionType

from . import utils

# Create your models here.
class Permission(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  type = models.CharField(choices=PermissionType, blank=False, null=False)
  data = models.ForeignKey(ShareableModel, on_delete=models.CASCADE)

  def save(self, **kwargs):
    if self.pk is None:
      permission_already_exists = Permission.objects.filter(
        user=self.user,
        data=self.data,
      ).exists()

      if permission_already_exists:
        return None

    return super().save(**kwargs)

  def delete(self, **kwargs):
    if self.data.type == DataType.FOLDER:
      utils.delete_access_to_notes_from_folder(self)
    return super().delete(**kwargs)