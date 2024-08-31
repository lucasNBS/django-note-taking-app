from django.contrib import admin
from .models import Permission

# Register your models here.
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
  list_display = ('user', 'type', 'data')
