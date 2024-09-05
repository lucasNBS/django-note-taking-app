from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Tag
from .forms import TagForm

# Create your views here.
class CreateTagView(CreateView):
  model = Tag
  template_name = 'tags/form.html'
  form_class = TagForm
  success_url = reverse_lazy('notes-list')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs["creator"] = self.request.user
    return kwargs

class UpdateTagView(UpdateView):
  model = Tag
  pk_url_kwarg = 'id'
  template_name = 'tags/form.html'
  form_class = TagForm
  success_url = reverse_lazy('notes-list')

class DeleteTagView(DeleteView):
  model = Tag
  pk_url_kwarg = 'id'
  template_name = 'tags/confirm_delete.html'
  success_url = reverse_lazy('notes-list')

def autocomplete_tag_view(request):
  search = request.GET.get('search')
  limit = 20

  tags = Tag.objects.filter(created_by=request.user).filter(
    Q(title__icontains=search) | Q(title__startswith=search)
  )

  response = [{'title': tag.title, 'id': tag.id} for tag in tags][:limit]

  return JsonResponse(response, safe=False)
