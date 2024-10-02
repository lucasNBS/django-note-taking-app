from django.urls import path, include
from .views import CreateFolder, UpdateFolder, DeleteFolder, autocomplete_folder_view

urlpatterns = [
  path("create", CreateFolder.as_view(), name='folders-create'),
  path("update/<int:id>", UpdateFolder.as_view(), name='folders-update'),
  path("delete/<int:id>", DeleteFolder.as_view(), name='folders-delete'),
  path("autocomplete", autocomplete_folder_view, name='folders-autocomplete'),
  path("api/", include('folders.api.urls')),
]
