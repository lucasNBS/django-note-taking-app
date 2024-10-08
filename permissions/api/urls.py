from django.urls import path, include
from rest_framework import routers
from .views import NotePermissionsView, FolderPermissionsView, DetailNotePermissionView, DetailFolderPermissionView, ListUserPermissionsView

urlpatterns = [
  path('note/<int:pk>/', NotePermissionsView.as_view()),
  path('note/permission/<int:pk>/', DetailNotePermissionView.as_view()),
  path('folder/<int:pk>/', FolderPermissionsView.as_view()),
  path('folder/permission/<int:pk>/', DetailFolderPermissionView.as_view()),
  path('user/', ListUserPermissionsView.as_view())
]
