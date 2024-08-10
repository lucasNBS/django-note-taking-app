from django.views.generic import View

class CreatedByUserFilter(View):
  
  def get_queryset(self, base_qs):
    return base_qs.filter(created_by=self.request.user)