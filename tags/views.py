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
