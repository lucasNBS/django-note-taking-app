from django.contrib import admin

from tags.models import Tag


@admin.register(Tag)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title",)
