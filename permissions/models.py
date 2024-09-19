from django.db import models
from accounts.models import User
from core.models import ShareableModel
from .choices import PermissionType

# Create your models here.
class Permission(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  type = models.CharField(choices=PermissionType, blank=False, null=False)
  data = models.ForeignKey(ShareableModel, on_delete=models.PROTECT)

  def save(self, **kwargs):
    if self.pk is None:
      permission_already_exists = Permission.objects.filter(
        user=self.user,
        data=self.data,
      ).exists()

      if permission_already_exists:
        return None

    return super().save(**kwargs)
