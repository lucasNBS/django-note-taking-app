from django.shortcuts import redirect
from tags.models import Tag
from folders.models import Folders
# from accounts.filters import CreatedByUserFilter
from django.views.generic import View
from permissions.models import Permission
from .choices import DataType

def redirect_home(request):
  return redirect('notes-list')

class BaseContext(View):

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["tags"] = Tag.objects.filter(created_by=self.request.user)

    foders_user_has_access_ids = Permission.objects.filter(user=self.request.user, data__type=DataType.FOLDER).values_list("data__id", flat=True)

    context["folders"] = Folders.objects.filter(id__in=foders_user_has_access_ids)
    return context