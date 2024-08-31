from django.db import models
from accounts.models import User
from core.models import ShareableModel

# Create your models here.
class Folders(ShareableModel):
  name = models.CharField(max_length=50)
  created_by = models.ForeignKey(User, on_delete=models.PROTECT)

  @classmethod
  def get_default_id(cls):
    folder, _ = cls.objects.get_or_create(
      name="General",
      created_by=User.objects.get(id=1)
    )
    return folder.id

  def __str__(self):
    return self.name