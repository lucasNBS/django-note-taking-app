from core.models import SoftDeleteModel
from django.db import models
from tags.models import Tag
from accounts.models import User
from folders.models import Folders
from core.models import ShareableModel

# Create your models here.
class Note(ShareableModel, SoftDeleteModel):
  title = models.CharField(max_length=50, blank=False, null=False)
  description = models.CharField(max_length=200, blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_liked = models.BooleanField(default=False)
  tags = models.ManyToManyField(Tag, blank=True, null=True)
  folder = models.ForeignKey(Folders, default=Folders.get_default_id, on_delete=models.PROTECT)
  created_by = models.ForeignKey(User, on_delete=models.PROTECT)

  def __str__(self) -> str:
    return self.title