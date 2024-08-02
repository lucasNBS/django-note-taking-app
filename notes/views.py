from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from notes.filters import FilterBaseModel
from notes.models import Note
from notes.forms import NoteForm, FavoriteNoteForm

class CreateNoteView(CreateView):
  model = Note
  template_name = 'notes/form.html'
  success_url = reverse_lazy('list')
  form_class = NoteForm

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["type"] = "Create"
    return context

class UpdateNoteView(UpdateView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/form.html'
  success_url = reverse_lazy('list')
  form_class = NoteForm

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["type"] = "Update"
    return context


class DeleteNoteView(DeleteView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/confirm_delete.html'
  success_url = reverse_lazy('list')

class DetailNoteView(DetailView):
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
  return redirect('list')

class FavoriteNoteView(UpdateView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/form.html'
  success_url = reverse_lazy('list')
  form_class = FavoriteNoteForm

class ListFavoriteNote(FilterBaseModel):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "Starred"

  def get_queryset(self):
    return super().get_queryset(base_qs=self.model.objects.filter(is_liked=True))
