from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from notes.models import Note
from notes.forms import NoteForm

class CreateNoteView(CreateView):
  model = Note
  template_name = 'notes/form.html'
  success_url = reverse_lazy('list')
  form_class = NoteForm

class UpdateNoteView(UpdateView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/form.html'
  success_url = reverse_lazy('list')
  form_class = NoteForm

class DeleteNoteView(DeleteView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/confirm_delete.html'
  success_url = reverse_lazy('list')

class DetailNoteView(DetailView):
  model = Note
  pk_url_kwarg = 'id'
  template_name = 'notes/note.html'

class ListNoteView(ListView):
  model = Note
  template_name = 'notes/notes.html'
  paginate_by = 20

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    print(context)

    return context