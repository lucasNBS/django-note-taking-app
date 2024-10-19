from django.views.generic import ListView
from tags.models import Tag
from core.views import BaseContext

from permissions.models import Permission
from core.choices import DataType

class FilterNoteBaseView(BaseContext, ListView):
  def get_queryset(self):
    user_permissions = Permission.objects.filter(user=self.request.user, data__type=DataType.NOTE)

    request = self.request.GET.copy()

    title = request.get('title', '')
    start_date = request.get('start-date', '')
    end_date = request.get('end-date', '')
    tags = request.pop('tags', '')

    user_permissions = user_permissions.filter(data__title__icontains=title)

    if start_date != "":
      user_permissions = user_permissions.filter(data__note__created_at__gte=start_date)

    if end_date != "":
      user_permissions = user_permissions.filter(data__note__created_at__lte=end_date)

    if len(tags) > 0:
      user_permissions = user_permissions.filter(data__note__tags__id__in=tags).distinct()

    return user_permissions.order_by('data__note__created_at')

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