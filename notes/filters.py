from django.views.generic import ListView
from .models import Note
from core.views import BaseContext

class FilterBaseModel(BaseContext, ListView):
  def get_queryset(self, base_qs=Note.objects.all()):
    title = self.request.GET.get('title', '')
    start_date = self.request.GET.get('start-date', '')
    end_date = self.request.GET.get('end-date', '')

    qs = base_qs.filter(title__icontains=title)

    if start_date != "":
      qs = qs.filter(created_at__gte=start_date)

    if end_date != "":
      qs = qs.filter(created_at__lte=end_date)

    return qs.order_by('created_at')
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    context["title"] = self.request.GET.get('title', '')
    context["start_date"] = self.request.GET.get('start-date', '')
    context["end_date"] = self.request.GET.get('end-date', '')

    return context