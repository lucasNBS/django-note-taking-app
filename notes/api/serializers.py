from rest_framework import serializers, exceptions

from accounts.api.utils import get_user
from permissions import models, choices
from tags.models import Tag 
from folders.models import Folders

from ..models import Note

class NoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Note
    exclude = ('type', 'is_deleted')
    extra_kwargs = {
      'id': {
        'read_only': True
      },
      'created_at': {
        'read_only': True
      },
      'updated_at': {
        'read_only': True
      },
    }

  def save(self):
    user = get_user(self.context['request'])

    tags = self.validated_data.get("tags", [])
    self._validate_tags(tags, user)

    folder = self.validated_data.get("folder", None)
    self._validate_folder(folder, user)

    super().save()

  def _validate_tags(self, tags, user):
    for tag in tags:
      if tag.created_by != user:
        raise exceptions.PermissionDenied("You do not have access to the selected tags")

  def _validate_folder(self, folder, user):
    # Allow user to create notes in 'General' folder
    if folder == Folders.objects.filter(title="General").first():
      return

    user_permission_to_folder = models.Permission.objects.filter(user=user, data=folder).first()
    if not user_permission_to_folder:
        raise exceptions.PermissionDenied("You do not have access to the selected folder")
    
    if user_permission_to_folder.type == choices.PermissionType.READER:
        raise exceptions.PermissionDenied(
          "You do not have permission to create notes in this folder"
        )
