from django.urls import path
from .views import ListNotePermissions, CreateNotePermissions, UpdateNotePermissions, RemoveNotePermissions

urlpatterns = [
  path("list/<int:note_id>", ListNotePermissions.as_view(), name='notes-permissions-list'),
  path("create/<int:note_id>", CreateNotePermissions.as_view(), name='notes-permissions-create'),
  path("update/<int:note_id>/<int:id>", UpdateNotePermissions.as_view(), name='notes-permissions-update'),
  path("remove/<int:note_id>/<int:id>", RemoveNotePermissions.as_view(), name='notes-permissions-remove'),
]
