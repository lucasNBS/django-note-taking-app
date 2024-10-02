from django.urls import path, include
from .views import CreateTagView, UpdateTagView, DeleteTagView, autocomplete_tag_view

urlpatterns = [
  path("create", CreateTagView.as_view(), name='tags-create'),
  path("update/<int:id>", UpdateTagView.as_view(), name='tags-update'),
  path("delete/<int:id>", DeleteTagView.as_view(), name='tags-delete'),
  path("autocomplete", autocomplete_tag_view, name='tags-autocomplete'),
  path("api/", include('tags.api.urls')),
]
