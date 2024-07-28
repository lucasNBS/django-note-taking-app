from core.models import SoftDeleteModel
from django.db import models

# Create your models here.
class Note(SoftDeleteModel):
  title = models.CharField(max_length=50, blank=False, null=False)
  description = models.CharField(max_length=200, blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_liked = models.BooleanField(default=False)

  def __str__(self) -> str:
    return self.title