from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.views import BaseContext
from core.choices import DataType

from . import models, forms, choices

class ListNotePermissions(BaseContext, ListView):
  model = models.Permission
  template_name = 'permissions/list.html'
  paginate_by = 20

  def get_queryset(self):
    id = self.kwargs["note_id"]
    return models.Permission.objects.filter(data__id=id).exclude(type=choices.PermissionType.CREATOR)
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["note_id"] = self.kwargs["note_id"]
    context["form"] = forms.PermissionCreateForm()
    return context

class CreateNotePermissions(CreateView):
  model = models.Permission
  template_name = 'permissions/form.html'
  form_class = forms.PermissionCreateForm

  def get_success_url(self):
    return f'/permissions/list/{self.kwargs["note_id"]}'
  
class UpdateNotePermissions(UpdateView):
  model = models.Permission
  template_name = 'permissions/form.html'
  pk_url_kwarg = 'id'
  form_class = forms.PermissionUpdateForm

  def get_success_url(self):
    return f'/permissions/list/{self.kwargs["note_id"]}'

class RemoveNotePermissions(DeleteView):
  model = models.Permission
  template_name = 'permissions/form.html'
  pk_url_kwarg = 'id'

  def get_success_url(self):
    return f'/permissions/list/{self.kwargs["note_id"]}'

  def post(self, request, **kwargs):
    if self.get_object().data.type == DataType.FOLDER:
      notes = models.Permission.objects.filter(
        user=self.get_object().user,
        data__type=DataType.NOTE,
        type=self.get_object().type,
        data__note__folder=self.get_object().data
      )

      for note in notes:
        note.delete()

    return super().post(self, request, **kwargs)
