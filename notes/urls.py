from django.urls import path
from .views import CreateNoteView, UpdateNoteView, DeleteNoteView, ListNoteView, DetailNoteView

urlpatterns = [
  path("create", CreateNoteView.as_view(), name='create'),
  path("update/<int:id>", UpdateNoteView.as_view(), name='update'),
  path("delete/<int:id>", DeleteNoteView.as_view(), name='delete'),
  path("<int:id>", DetailNoteView.as_view(), name='detail'),
  path("", ListNoteView.as_view(), name='list'),
]
