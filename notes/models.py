from core.models import SoftDeleteModel
from django.db import models
from tags.models import Tag
from folders.models import Folders
from core.models import ShareableModel
from core.choices import DataType
from accounts.models import User

# Create your models here.
class Note(SoftDeleteModel, ShareableModel):
  description = models.CharField(max_length=200, blank=False, null=False)
  content = models.TextField(blank=False, null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  tags = models.ManyToManyField(Tag, blank=True)
  folder = models.ForeignKey(Folders, default=Folders.get_default_id, on_delete=models.CASCADE)

  def save(self, **kwargs):
    self.type = DataType.NOTE
    return super().save(**kwargs)
  
class Like(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  note = models.ForeignKey(Note, on_delete=models.CASCADE)

  def save(self, **kwargs):
    if self.pk is None:
      like_already_exists = Like.objects.filter(
        user=self.user,
        note=self.note,
      ).exists()

      if like_already_exists:
        return None

    return super().save(**kwargs)
