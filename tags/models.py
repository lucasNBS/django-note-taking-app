from django.db import models
from accounts.models import User

# Create your models here.
class Tag(models.Model):
  name = models.CharField(max_length=50)
  created_by = models.ForeignKey(User, on_delete=models.PROTECT)

  def __str__(self) -> str:
    return self.name