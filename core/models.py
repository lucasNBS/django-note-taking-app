from core.managers import SoftDeleteManager
from django.db import models
from .choices import DataType

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
  title = models.CharField(max_length=50, blank=False, null=False)
  type = models.CharField(choices=DataType, blank=False, null=False)

  def __str__(self):
    return self.title
