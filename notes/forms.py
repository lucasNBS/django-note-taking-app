from django import forms
from notes.models import Note

class NoteForm(forms.ModelForm):

  class Meta:
    model = Note
    fields = '__all__'
    widgets = {
      'title': forms.TextInput(),
      'content': forms.Textarea(),
    }