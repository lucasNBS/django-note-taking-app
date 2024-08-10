from django import forms
from django.core.exceptions import ValidationError
from core.widgets import InputField
from .models import Folders

class FolderForm(forms.ModelForm):
  name = forms.CharField(widget=InputField(label='Name'))

  class Meta:
    model = Folders
    fields = ('name',)

  def __init__(self, creator=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.creator = creator

  def clean_name(self):
    name = self.cleaned_data["name"]
    if len(name) > 50:
      raise ValidationError("Max length is 50")
    return name
  
  def save(self, *args, **kwargs):
    if self.creator is not None:
      self.instance.created_by = self.creator    
    return super().save(*args, **kwargs)