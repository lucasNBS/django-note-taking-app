from django.db.models import Q
from django.db.models.base import Model as Model
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from core.views import BaseContext
from notes.filters import FilterBaseView
from notes.models import Note, Like
from notes.forms import NoteForm, FavoriteNoteForm
from core.choices import DataType
from tags.models import Tag
from folders.models import Folders
from permissions.models import Permission
from permissions.choices import PermissionType
from core.choices import DataType

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

class ListNoteView(FilterBaseView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "All Notes"

  def get_queryset(self):
    return super().get_queryset(base_qs=self.model.objects)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    likes_id = Like.objects.filter(user=self.request.user).values_list('note__id', flat=True)
    context["likes_id"] = likes_id
    return context

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
  permission_exists = Permission.objects.filter(
    user=request.user, data__type=DataType.NOTE, data__id=id
  ).exists()
  if permission_exists:
    note = Note.all_objects.filter(is_deleted=True).get(id=id)
    note.restore()
  return redirect('notes-list')

class FavoriteNoteView(CreateView):
  model = Like
  template_name = 'notes/form.html'
  success_url = reverse_lazy('notes-list')

  def get_form(self):
    form = super().get_form(FavoriteNoteForm)
    data = form.data.copy()
    data['user'] = self.request.user
    data['note'] = self.kwargs.get('id')
    form.data = data
    return form

class ListFavoriteNoteView(FilterBaseView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "Starred"
  liked = True

  def get_queryset(self):
    likes_id = Like.objects.filter(user=self.request.user).values_list('note__id', flat=True)
    return super().get_queryset(base_qs=self.model.objects.filter(id__in=likes_id))

class ListTagNotesView(FilterBaseView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20

  def get_queryset(self):
    tag = get_object_or_404(
      Tag.objects.filter(created_by=self.request.user), id=self.kwargs.get('id')
    )
    self.title = tag.title
    return super().get_queryset(base_qs=self.model.objects.filter(tags__id=tag.id))

class ListFolderNotesView(FilterBaseView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20

  def get_queryset(self):
    permission_exists = Permission.objects.filter(
      user=self.request.user, data__type=DataType.FOLDER, data__id=self.kwargs.get('id')
    ).exists()
    if permission_exists:
      folder = Folders.objects.get(id=self.kwargs.get('id'))
      self.title = folder.title
      notes = Note.objects.filter(folder=folder)
      return super().get_queryset(base_qs=notes)

class ListSharedNoteView(FilterBaseView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "Shared"

  def get_queryset(self):
    notes_user_has_access = Permission.objects.filter(
      user=self.request.user, data__type=DataType.NOTE
    ).filter(
      Q(type=PermissionType.EDITOR) | Q(type=PermissionType.READER)
    ).values_list("data__id", flat=True)
    return super().get_queryset(base_qs=self.model.objects.filter(id__in=notes_user_has_access))
