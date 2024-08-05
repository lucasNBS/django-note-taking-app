from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from core.views import BaseContext
from notes.filters import FilterBaseModel
from notes.models import Note
from notes.forms import NoteForm, FavoriteNoteForm
from tags.models import Tag

class CreateNoteView(BaseContext, CreateView):
  model = Note
  template_name = 'notes/form.html'
  success_url = reverse_lazy('notes-list')
  form_class = NoteForm

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["type"] = "Create"
    return context

class UpdateNoteView(BaseContext, UpdateView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/form.html'
  success_url = reverse_lazy('notes-list')
  form_class = NoteForm

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["type"] = "Update"
    return context

class DeleteNoteView(DeleteView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/confirm_delete.html'
  success_url = reverse_lazy('notes-list')

class DetailNoteView(BaseContext, DetailView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/note.html'

class ListNoteView(FilterBaseModel):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "All Notes"

class ListDeletedNoteView(FilterBaseModel):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "Trash"

  def get_queryset(self):
    return super().get_queryset(base_qs=self.model.all_objects.filter(is_deleted=True))
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["deleted"] = True
    return context

def restore_note_view(request, id):
  note = Note.all_objects.get(id=id)
  note.restore()
  return redirect('notes-list')

class FavoriteNoteView(BaseContext, UpdateView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/form.html'
  success_url = reverse_lazy('notes-list')
  form_class = FavoriteNoteForm

class ListFavoriteNoteView(FilterBaseModel):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "Starred"

  def get_queryset(self):
    return super().get_queryset(base_qs=self.model.objects.filter(is_liked=True))

class ListTagNotesView(FilterBaseModel):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20

  def get_queryset(self):
    tag = get_object_or_404(Tag, id=self.kwargs.get('id'))
    self.title = tag.name
    return super().get_queryset(base_qs=self.model.objects.filter(tags__id=tag.id))
