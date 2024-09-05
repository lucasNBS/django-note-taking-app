from django import forms
from django.core.exceptions import ValidationError
from core.widgets import InputField
from .models import Tag

class TagForm(forms.ModelForm):
  title = forms.CharField(widget=InputField(label='Title'))

  class Meta:
    model = Tag
    fields = ['title',]

  def __init__(self, creator=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.creator = creator

  def clean_title(self):
    title = self.cleaned_data["title"]
    if len(title) > 50:
      raise ValidationError("Max length is 50")
    return title

  def save(self, *args, **kwargs):
    if self.creator is not None:
      self.instance.created_by = self.creator
    return super().save(*args, **kwargs)