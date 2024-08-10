from django import forms
from django.core.exceptions import ValidationError
from notes.models import Note
from core import widgets

class NoteForm(forms.ModelForm):
  title = forms.CharField(widget=widgets.InputField(label="Title"))
  description = forms.CharField(widget=widgets.InputField(label="Description"))
  content = forms.CharField(widget=widgets.Textarea(label="Content"))

  class Meta:
    model = Note
    fields = ['title', 'description', 'tags', 'content']
    widgets = {
      'tags': widgets.SelectMultiple(label="Tags")
    }

  def __init__(self, creator=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.creator = creator

  def clean_title(self):
    title = self.cleaned_data["title"]
    if len(title) > 50:
      raise ValidationError("Max length is 50")
    return title

  def clean_description(self):
    description = self.cleaned_data["description"]
    if len(description) > 200:
      raise ValidationError("Max length is 200")
    return description
  
  def save(self, *args, **kwargs):
    if self.creator is not None:
      self.instance.created_by = self.creator
    return super().save(*args, **kwargs)

class FavoriteNoteForm(forms.ModelForm):
  
  class Meta:
    model = Note
    fields = ['is_liked',]