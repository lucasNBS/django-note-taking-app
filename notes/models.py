from core.models import SoftDeleteModel
from django.db import models
from tags.models import Tag
from folders.models import Folders
from core.models import ShareableModel
from core.choices import DataType

# Create your models here.
class Note(SoftDeleteModel, ShareableModel):
  description = models.CharField(max_length=200, blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_liked = models.BooleanField(default=False)
  tags = models.ManyToManyField(Tag, blank=True, null=True)
  folder = models.ForeignKey(Folders, default=Folders.get_default_id, on_delete=models.PROTECT)

  def save(self, **kwargs):
    self.type = DataType.NOTE
    return super().save(**kwargs)