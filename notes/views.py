from django.db.models.base import Model as Model
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from core.views import BaseContext
from notes.filters import FilterBaseView
from notes.models import Note
from notes.forms import NoteForm, FavoriteNoteForm
from tags.models import Tag
from folders.models import Folders
from accounts.filters import CreatedByUserFilter

class CreateNoteView(BaseContext, CreateView):
  model = Note
  template_name = 'notes/form.html'
  success_url = reverse_lazy('notes-list')
  form_class = NoteForm

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["type"] = "Create"
    return context
  
  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs["creator"] = self.request.user
    return kwargs
  
  def get_queryset(self):
    return super().get_queryset(self.model.objects.all())

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
  
  def get_queryset(self):
    return super().get_queryset(self.model.objects.all())

class DeleteNoteView(CreatedByUserFilter, DeleteView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/confirm_delete.html'
  success_url = reverse_lazy('notes-list')
  
  def get_queryset(self):
    return super().get_queryset(self.model.objects.all())

class DetailNoteView(BaseContext, DetailView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/note.html'

  def get_queryset(self):
    return super().get_queryset(self.model.objects.all())

class ListNoteView(FilterBaseView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "All Notes"

class ListDeletedNoteView(FilterBaseView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "Trash"
  deactivate = True

  def get_queryset(self):
    return super().get_queryset(base_qs=self.model.all_objects.filter(is_deleted=True))
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["deleted"] = True
    return context

def restore_note_view(request, id):
  note = Note.all_objects.filter(created_by=request.user).get(id=id)
  note.restore()
  return redirect('notes-list')

class FavoriteNoteView(BaseContext, UpdateView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/form.html'
  success_url = reverse_lazy('notes-list')
  form_class = FavoriteNoteForm

  def get_queryset(self):
    return super().get_queryset(self.model.objects.all())

class ListFavoriteNoteView(FilterBaseView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "Starred"

  def get_queryset(self):
    return super().get_queryset(base_qs=self.model.objects.filter(is_liked=True))

class ListTagNotesView(FilterBaseView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20

  def get_queryset(self):
    tag = get_object_or_404(
      Tag.objects.filter(created_by=self.request.user), id=self.kwargs.get('id')
    )
    self.title = tag.name
    return super().get_queryset(base_qs=self.model.objects.filter(tags__id=tag.id))

class ListFolderNotesView(FilterBaseView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20

  def get_queryset(self):
    folder = get_object_or_404(
      Folders.objects.filter(created_by=self.request.user), id=self.kwargs.get('id')
    )
    self.title = folder.name
    return super().get_queryset(base_qs=self.model.objects.filter(folder__id=folder.id))
