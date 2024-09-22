from django import forms
from django.core.exceptions import ValidationError
from core.widgets import InputField
from permissions import choices, models
from .models import Folders

class FolderForm(forms.ModelForm):
  title = forms.CharField(widget=InputField(label='Title'))

  class Meta:
    model = Folders
    fields = ('title',)

  def __init__(self, creator=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.creator = creator

  def clean_title(self):
    title = self.cleaned_data["title"]
    if len(title) > 50:
      raise ValidationError("Max length is 50")
    return title
  
  def save(self, *args, **kwargs):
    save = super().save(*args, **kwargs)

    permission_already_exists = models.Permission.objects.filter(
      type=choices.PermissionType.CREATOR, data=self.instance
    ).exists()

    if not permission_already_exists:
      models.Permission.objects.create(
        user=self.creator, type=choices.PermissionType.CREATOR, data=self.instance
      )

    return save