from django.db.models import Q
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models.base import Model as Model
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from core.views import BaseContext
from notes.filters import FilterNoteBaseView
from notes.models import Note, Like
from notes.forms import NoteForm, UpdateSharedNoteForm, FavoriteNoteForm
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

  def get_form_class(self):
    permission = Permission.objects.get(
      user=self.request.user,
      data__type=DataType.NOTE,
      data=self.get_object(),
    )

    if permission.type != PermissionType.CREATOR:
      return UpdateSharedNoteForm

    return NoteForm
  
  def get_object(self, **kwargs):
    obj = super().get_object(**kwargs)

    permission = Permission.objects.filter(
      user=self.request.user,
      data__id=obj.id,
      data__note__is_deleted=False,
      data__type=DataType.NOTE,
    ).exclude(type=PermissionType.READER).exists()

    if not permission:
      raise PermissionDenied("You cannot perform this action")

    return obj

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["type"] = "Update"
    return context

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs["creator"] = self.request.user
    return kwargs

class DeleteNoteView(DeleteView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/confirm_delete.html'
  success_url = reverse_lazy('notes-list')

  def get_object(self, **kwargs):
    obj = super().get_object(**kwargs)

    permission = Permission.objects.filter(
      user=self.request.user,
      data__id=obj.id,
      data__note__is_deleted=False,
      data__type=DataType.NOTE,
      type=PermissionType.CREATOR,
    ).exists()

    if not permission:
      raise PermissionDenied("You cannot perform this action")

    return obj

class DetailNoteView(BaseContext, DetailView):
  pk_url_kwarg = 'id'
  template_name = 'notes/note.html'

  def get_object(self):
    permission = Permission.objects.filter(
      user=self.request.user,
      data__type=DataType.NOTE,
      data__note__is_deleted=False,
      data__id=self.kwargs.get('id')
    ).first()

    if not permission:
      raise PermissionDenied("You do not have permission to access this note")

    return permission

class ListNoteView(FilterNoteBaseView):
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "All Notes"

  def get_queryset(self):
    permissions_of_notes_user_has_access = super().get_queryset()
    return permissions_of_notes_user_has_access.filter(data__note__is_deleted=False)

class ListDeletedNoteView(FilterNoteBaseView):
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "Trash"
  deactivate = True

  def get_queryset(self):
    permissions_of_notes_user_has_access = super().get_queryset()
    permissions_of_deleted_notes_user_has_access = permissions_of_notes_user_has_access.filter(
      data__note__is_deleted=True
    )
    return permissions_of_deleted_notes_user_has_access
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["deleted"] = True
    return context

def restore_note_view(request, id):
  permission_exists = Permission.objects.filter(
    user=request.user,
    data__type=DataType.NOTE,
    data__note__is_deleted=True,
    data__id=id,
    type=PermissionType.CREATOR,
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

class ListFavoriteNoteView(FilterNoteBaseView):
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "Starred"

  def get_queryset(self):
    permissions_of_notes_user_has_access = super().get_queryset()
    permissions_of_non_deleted_notes_user_has_access = permissions_of_notes_user_has_access.filter(
      data__note__is_deleted=False
    )

    permissions_ids_of_notes_user_has_liked = []

    for permission in permissions_of_non_deleted_notes_user_has_access:
      if permission.data.note.like_set.filter(user=self.request.user).exists():
        permissions_ids_of_notes_user_has_liked.append(permission.id)

    return permissions_of_non_deleted_notes_user_has_access.filter(
      id__in=permissions_ids_of_notes_user_has_liked
    )

class ListTagNotesView(FilterNoteBaseView):
  template_name = 'notes/notes.html'
  paginate_by = 20

  def get_queryset(self):
    permissions_of_notes_user_has_access = super().get_queryset()

    tag = get_object_or_404(
      Tag.objects.filter(created_by=self.request.user), id=self.kwargs.get('id')
    )
    self.title = tag.title

    return permissions_of_notes_user_has_access.filter(
      data__note__is_deleted=False, data__note__tags__id=tag.id
    )

class ListFolderNotesView(FilterNoteBaseView):
  template_name = 'notes/notes.html'
  paginate_by = 20

  def get_queryset(self):
    folder = get_object_or_404(
      Folders.objects.filter(id=self.kwargs.get('id')), id=self.kwargs.get('id')
    )

    permission_exists = Permission.objects.filter(
      user=self.request.user, data__type=DataType.FOLDER, data__id=self.kwargs.get('id')
    ).exists()
    if permission_exists:
      permissions_of_notes_user_has_access = super().get_queryset()

      self.title = folder.title

      return permissions_of_notes_user_has_access.filter(
        data__note__is_deleted=False, data__note__folder=folder
      )
    raise PermissionDenied("You do not have permission to access this folder")

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["folder"] = Permission.objects.filter(
      user=self.request.user,
      data__type=DataType.FOLDER,
      data__id=self.kwargs.get('id'),
      type=PermissionType.CREATOR,
    ).first()
    return context

class ListSharedNoteView(FilterNoteBaseView):
  template_name = 'notes/notes.html'
  paginate_by = 20
  title = "Shared"

  def get_queryset(self):
    permissions_of_notes_user_has_access = super().get_queryset()
    return permissions_of_notes_user_has_access.filter(data__note__is_deleted=False).filter(
      Q(type=PermissionType.EDITOR) | Q(type=PermissionType.READER)
    )
