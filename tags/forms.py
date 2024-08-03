from django import forms
from django.core.exceptions import ValidationError
from core.widgets import InputField
from .models import Tag

class TagForm(forms.ModelForm):
  name = forms.CharField(widget=InputField(label='Name'))

  class Meta:
    model = Tag
    fields = ['name',]

  def clean_name(self):
    title = self.cleaned_data["name"]
    if len(title) > 50:
      raise ValidationError("Max length is 50")
    return title