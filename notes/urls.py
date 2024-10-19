from django.urls import include, path

from .views import (
    CreateNoteView,
    DeleteNoteView,
    DetailNoteView,
    FavoriteNoteView,
    ListDeletedNoteView,
    ListFavoriteNoteView,
    ListFolderNotesView,
    ListNoteView,
    ListSharedNoteView,
    ListTagNotesView,
    UpdateNoteView,
    restore_note_view,
)

urlpatterns = [
    path("create", CreateNoteView.as_view(), name="notes-create"),
    path("update/<int:id>", UpdateNoteView.as_view(), name="notes-update"),
    path("delete/<int:id>", DeleteNoteView.as_view(), name="notes-delete"),
    path("<int:id>", DetailNoteView.as_view(), name="notes-detail"),
    path("", ListNoteView.as_view(), name="notes-list"),
    path("restore/<int:id>", restore_note_view, name="notes-restore"),
    path("starred/<int:id>", FavoriteNoteView.as_view(), name="notes-starred"),
    path("starred", ListFavoriteNoteView.as_view(), name="notes-starreds"),
    path("trash", ListDeletedNoteView.as_view(), name="notes-list-deleted"),
    path("tag/<int:id>", ListTagNotesView.as_view(), name="notes-list-tag"),
    path("folder/<int:id>", ListFolderNotesView.as_view(), name="notes-list-folder"),
    path("shared", ListSharedNoteView.as_view(), name="notes-shared"),
    path("api/", include("notes.api.urls")),
]
