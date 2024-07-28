from django import forms
from notes.models import Note
from core import widgets

class NoteForm(forms.ModelForm):
  title = forms.CharField(widget=widgets.InputField(label="Title"))
  content = forms.CharField(widget=widgets.Textarea(label="Content"))

  class Meta:
    model = Note
    fields = ['title', 'content']
