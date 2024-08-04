from django.urls import path
from .views import CreateNoteView, UpdateNoteView, DeleteNoteView, ListNoteView, DetailNoteView, ListDeletedNoteView, restore_note_view, FavoriteNoteView, ListFavoriteNoteView, ListTagNotesView

urlpatterns = [
  path("create", CreateNoteView.as_view(), name='notes-create'),
  path("update/<int:id>", UpdateNoteView.as_view(), name='notes-update'),
  path("delete/<int:id>", DeleteNoteView.as_view(), name='notes-delete'),
  path("<int:id>", DetailNoteView.as_view(), name='notes-detail'),
  path("", ListNoteView.as_view(), name='notes-list'),
  path("restore/<int:id>", restore_note_view, name='notes-restore'),
  path("starred/<int:id>", FavoriteNoteView.as_view(), name='notes-starred'),
  path("starred", ListFavoriteNoteView.as_view(), name='notes-starreds'),
  path("trash", ListDeletedNoteView.as_view(), name='notes-list-deleted'),
  path("tag/<int:id>", ListTagNotesView.as_view(), name='notes-list-tag'),
]
