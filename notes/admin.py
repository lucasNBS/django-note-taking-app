from django.contrib import admin
from notes.models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
  list_display = ('title', 'content', 'created_at', 'updated_at', 'is_liked')
  readonly_fields = ('created_at', 'updated_at')