from django.contrib import admin
from .models import Folders

# Register your models here.
@admin.register(Folders)
class FoldersAdmin(admin.ModelAdmin):
  list_display = ('name', 'created_by')