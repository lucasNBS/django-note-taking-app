from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Folders
from .forms import FolderForm
from accounts.filters import CreatedByUserFilter

# Create your views here.
class CreateFolder(CreateView):
  model = Folders
  template_name = 'folders/form.html'
  form_class = FolderForm
  success_url = reverse_lazy('notes-list')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs["creator"] = self.request.user
    return kwargs
  
class UpdateFolder(CreatedByUserFilter, UpdateView):
  model = Folders
  template_name = 'folders/form.html'
  form_class = FolderForm
  success_url = reverse_lazy('notes-list')
  pk_url_kwarg = 'id'

  def get_queryset(self):
    return super().get_queryset(self.model.objects.all())

class DeleteFolder(CreatedByUserFilter, DeleteView):
  model = Folders
  template_name = 'folders/confirm_delete.html'
  success_url = reverse_lazy('notes-list')
  pk_url_kwarg = 'id'

  def get_queryset(self):
    return super().get_queryset(self.model.objects.all())

def autocomplete_folder_view(request):
  search = request.GET.get('search')
  limit = 20

  folders = Folders.objects.filter(created_by=request.user).filter(
    Q(name__icontains=search) | Q(name__startswith=search)
  )

  response = [{'name': folder.name, 'id': folder.id} for folder in folders][:limit]

  return JsonResponse(response, safe=False)
