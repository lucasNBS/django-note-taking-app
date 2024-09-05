from core.models import ShareableModel
from core.choices import DataType

# Create your models here.
class Folders(ShareableModel):

  @classmethod
  def get_default_id(cls):
    folder, _ = cls.objects.get_or_create(
      title="General"
    )
    return folder.id
  
  def save(self, **kwargs):
    self.type = DataType.FOLDER
    return super().save(**kwargs)