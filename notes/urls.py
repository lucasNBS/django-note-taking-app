from django.urls import path
from .views import CreateNoteView, UpdateNoteView, DeleteNoteView, ListNoteView, DetailNoteView, ListDeletedNoteView, restore_note_view, FavoriteNoteView, ListFavoriteNote

urlpatterns = [
  path("create", CreateNoteView.as_view(), name='create'),
  path("update/<int:id>", UpdateNoteView.as_view(), name='update'),
  path("delete/<int:id>", DeleteNoteView.as_view(), name='delete'),
  path("<int:id>", DetailNoteView.as_view(), name='detail'),
  path("", ListNoteView.as_view(), name='list'),
  path("restore/<int:id>", restore_note_view, name='restore'),
  path("favorite/<int:id>", FavoriteNoteView.as_view(), name='favorite'),
  path("favorites", ListFavoriteNote.as_view(), name='favorites'),
  path("trash", ListDeletedNoteView.as_view(), name='list-deleted'),
]
