from django.views.generic import ListView
from .models import Note
from tags.models import Tag
from core.views import BaseContext

class FilterBaseView(BaseContext, ListView):
  def get_queryset(self, base_qs=Note.objects.all()):
    request = self.request.GET.copy()

    title = request.get('title', '')
    start_date = request.get('start-date', '')
    end_date = request.get('end-date', '')
    tags = request.pop('tags', '')

    qs = base_qs.filter(created_by=self.request.user)

    qs = qs.filter(title__icontains=title)

    if start_date != "":
      qs = qs.filter(created_at__gte=start_date)

    if end_date != "":
      qs = qs.filter(created_at__lte=end_date)

    if len(tags) > 0:
      qs = qs.filter(tags__id__in=tags).distinct()

    return qs.order_by('created_at')
  
  def get_context_data(self, **kwargs):
    request = self.request.GET.copy()
    context = super().get_context_data(**kwargs)

    context["title"] = request.get('title', '')
    context["start_date"] = request.get('start-date', '')
    context["end_date"] = request.get('end-date', '')

    tags_selected = request.pop('tags', '')

    tags = Tag.objects.filter(id__in=tags_selected).distinct()

    context["tags_selected"] = [{ 'name': tag.name, 'value': tag.id } for tag in tags]
    context["filter_variant"] = True

    return context