from core.managers import SoftDeleteManager
from django.db import models

class SoftDeleteModel(models.Model):
  is_deleted = models.BooleanField(default=False)
  objects = SoftDeleteManager()
  all_objects = models.Manager()

  def delete(self):
    self.is_deleted = True
    self.save()

  def restore(self):
    self.is_deleted = False
    self.save()

  class Meta:
    abstract = True

class ShareableModel(models.Model):
  id = models.AutoField(primary_key=True)
