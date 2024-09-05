from django.contrib import admin
from notes.models import Note, Like

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
  list_display = ('title', 'is_deleted', 'content', 'created_at', 'updated_at')
  readonly_fields = ('created_at', 'updated_at')

  def get_queryset(self, request):
    qs = Note.all_objects.all()
    return qs
  
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
  list_display = ('user', 'note')
