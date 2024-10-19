from core.choices import DataType
from folders.models import Folders

from . import models, constants

def delete_access_to_notes_from_folder(folder_permission):
  notes_permissions = models.Permission.objects.filter(
      user=folder_permission.user,
      data__type=DataType.NOTE,
      type=folder_permission.type,
      data__note__folder=folder_permission.data
    )

  for permission in notes_permissions:
    permission.delete()

def create_access_to_notes_from_folder(folder_permission):
  folder_notes = Folders.objects.get(id=folder_permission.data.id).note_set.all()
  update_access_to_notes_from_folder(folder_permission)

  for note in folder_notes:
    permission_exists = models.Permission.objects.filter(
      user=folder_permission.user, data=note
    ).exists()

    if not permission_exists:
      models.Permission.objects.create(
        data=note, user=folder_permission.user, type=folder_permission.type
      )

def update_access_to_notes_from_folder(folder_permission):
  notes_of_folder_permissions = models.Permission.objects.filter(
    user=folder_permission.user,
    data__type=DataType.NOTE,
    type=folder_permission.type,
    data__note__folder=folder_permission.data
  )
  if notes_of_folder_permissions.exists():
    notes_of_folder_permissions.update(type=constants.permissions_relation[folder_permission.type])
