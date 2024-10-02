from rest_framework import serializers

from accounts.api.utils import get_user
from permissions import models, choices

from ..models import Folders

class FoldersSerializer(serializers.ModelSerializer):
  class Meta:
    model = Folders
    fields = ('id', 'title')
    extra_kwargs = {
      'id': {
        'read_only': True
      },
    }

  def create(self, validated_data):
    instance = self.Meta.model(**validated_data)
    instance.save()
    models.Permission.objects.create(
      user=get_user(self.context['request']),
      type=choices.PermissionType.CREATOR,
      data=instance,
    )
    return instance