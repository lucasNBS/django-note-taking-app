from permissions import models, choices
from .models import Folders

def is_general_folder(folder):
  return folder.id == Folders.objects.filter(title="General").first().id

def create_permission_to_folder_user_has_just_created(folder, user):
  models.Permission.objects.create(
    user=user, type=choices.PermissionType.CREATOR, data=folder
  )