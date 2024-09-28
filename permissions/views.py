from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.http import Http404

from core.views import BaseContext
from core.choices import DataType

from . import models, forms, choices

def verify_user_permission(self):
  id = self.kwargs["data_id"]

  permission_exists = models.Permission.objects.filter(
    user=self.request.user,
    data__id=id,
    type=choices.PermissionType.CREATOR,
  ).filter(
    Q(data__type=DataType.NOTE, data__note__is_deleted=False) | Q(data__type=DataType.FOLDER)
  ).exists()

  if not permission_exists:
    raise PermissionDenied("You cannot perform this action")

class ListPermissions(BaseContext, ListView):
  model = models.Permission
  template_name = 'permissions/list.html'
  paginate_by = 20

  def get(self, request, **kwargs):
    verify_user_permission(self)
    return super().get(request, **kwargs)

  def get_queryset(self):
    id = self.kwargs["data_id"]
    return models.Permission.objects.filter(data__id=id).exclude(type=choices.PermissionType.CREATOR)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["data_id"] = self.kwargs["data_id"]
    context["form"] = forms.PermissionCreateForm()
    return context

class CreatePermissions(CreateView):
  model = models.Permission
  template_name = 'permissions/form.html'
  form_class = forms.PermissionCreateForm

  def get_success_url(self):
    return f'/permissions/list/{self.kwargs["data_id"]}'

  def form_valid(self, form):
    verify_user_permission(self)
    return super().form_valid(form)
  
class UpdatePermissions(UpdateView):
  model = models.Permission
  template_name = 'permissions/form.html'
  pk_url_kwarg = 'id'
  form_class = forms.PermissionUpdateForm

  def get_success_url(self):
    return f'/permissions/list/{self.kwargs["data_id"]}'

  def form_valid(self, form):
    verify_user_permission(self)
    return super().form_valid(form)

class DeletePermissions(DeleteView):
  model = models.Permission
  template_name = 'permissions/form.html'
  pk_url_kwarg = 'id'

  def get_success_url(self):
    return f'/permissions/list/{self.kwargs["data_id"]}'

  def _delete_notes_from_folder(self, obj):
    notes = models.Permission.objects.filter(
        user=obj.user,
        data__type=DataType.NOTE,
        type=obj.type,
        data__note__folder=obj.data
      )

    for note in notes:
      note.delete()

  def post(self, request, **kwargs):
    obj = self.get_object()

    verify_user_permission(self)
    post = super().post(self, request, **kwargs)

    if obj.data.type == DataType.FOLDER:
      self._delete_notes_from_folder(obj)

    return post
