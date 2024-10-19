from django import forms
from django.core.exceptions import ValidationError
from core.widgets import InputField
from permissions import choices, models
from .models import Folders
from . import utils

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
    already_created = True if self.instance.id else None

    save = super().save(*args, **kwargs)

    if self.creator is not None and not already_created:
      utils.create_permission_to_folder_user_has_just_created(self.instance, self.creator)

    return save