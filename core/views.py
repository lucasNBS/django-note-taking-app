from django.shortcuts import redirect
from django.views.generic import View
from tags.models import Tag

def redirect_home(request):
  return redirect('notes-list')

class BaseContext(View):

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["tags"] = Tag.objects.filter(created_by=self.request.user)
    return context