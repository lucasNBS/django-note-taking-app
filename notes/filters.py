from django.views.generic import ListView
from tags.models import Tag
from core.views import BaseContext

from permissions.models import Permission
from core.choices import DataType

class FilterBaseView(BaseContext, ListView):
  def get_queryset(self, base_qs):
    notes_user_has_access_ids = Permission.objects.filter(
      user=self.request.user, data__type=DataType.NOTE
    ).values_list("data__id", flat=True)
    notes = base_qs.filter(id__in=notes_user_has_access_ids)

    request = self.request.GET.copy()

    title = request.get('title', '')
    start_date = request.get('start-date', '')
    end_date = request.get('end-date', '')
    tags = request.pop('tags', '')

    notes = notes.filter(title__icontains=title)

    if start_date != "":
      notes = notes.filter(created_at__gte=start_date)

    if end_date != "":
      notes = notes.filter(created_at__lte=end_date)

    if len(tags) > 0:
      notes = notes.filter(tags__id__in=tags).distinct()

    return notes.order_by('created_at')
  
  def get_context_data(self, **kwargs):
    request = self.request.GET.copy()
    context = super().get_context_data(**kwargs)

    context["title"] = request.get('title', '')
    context["start_date"] = request.get('start-date', '')
    context["end_date"] = request.get('end-date', '')

    tags_selected = request.pop('tags', '')

    tags = Tag.objects.filter(id__in=tags_selected).distinct()

    context["tags_selected"] = [{ 'title': tag.title, 'value': tag.id } for tag in tags]
    context["filter_variant"] = True

    return context