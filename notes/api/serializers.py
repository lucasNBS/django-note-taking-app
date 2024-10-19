from rest_framework import serializers, exceptions

from accounts.api.utils import get_user
from permissions import models, choices
from tags.models import Tag 
from folders.models import Folders
from folders.utils import is_general_folder

from ..models import Note
from .. import utils

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

  def create(self, validated_data):
    user = get_user(self.context['request'])
    tags = validated_data.pop("tags")

    instance = Note(**validated_data)
    instance.save()
    utils.create_permission_to_note_user_has_just_created(instance, user)
    instance.tags.set(tags)
    return instance

  def validate_tags(self, tags):
    user = get_user(self.context['request'])

    for tag in tags:
      if tag.created_by != user:
        raise exceptions.PermissionDenied("You do not have access to the selected tags")

    return tags

  def validate_folder(self, folder):
    user = get_user(self.context['request'])

    # Allow user to create notes in 'General' folder
    if is_general_folder(folder):
      return folder

    user_permission_to_folder = models.Permission.objects.filter(user=user, data=folder).first()
    if not user_permission_to_folder:
        raise exceptions.PermissionDenied("You do not have access to the selected folder")
    
    if user_permission_to_folder.type == choices.PermissionType.READER:
        raise exceptions.PermissionDenied(
          "You do not have permission to create notes in this folder"
        )

    return folder
