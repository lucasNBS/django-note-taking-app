from django.shortcuts import redirect
from tags.models import Tag
from accounts.filters import CreatedByUserFilter

def redirect_home(request):
  return redirect('notes-list')

class BaseContext(CreatedByUserFilter):

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["tags"] = Tag.objects.filter(created_by=self.request.user)
    return context