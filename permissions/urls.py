from django.urls import path, include
from .views import ListPermissions, CreatePermissions, UpdatePermissions, DeletePermissions

urlpatterns = [
  path("list/<int:data_id>", ListPermissions.as_view(), name='notes-permissions-list'),
  path("create/<int:data_id>", CreatePermissions.as_view(), name='notes-permissions-create'),
  path("update/<int:data_id>/<int:id>", UpdatePermissions.as_view(), name='notes-permissions-update'),
  path("remove/<int:data_id>/<int:id>", DeletePermissions.as_view(), name='notes-permissions-remove'),
  path("api/", include('permissions.api.urls')),
]
