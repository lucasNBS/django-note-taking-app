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
    fields = ['title', 'description', 'content']

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

class FavoriteNoteForm(forms.ModelForm):
  
  class Meta:
    model = Note
    fields = ['is_liked',]