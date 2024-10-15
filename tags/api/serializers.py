from rest_framework import serializers

from accounts.api.utils import get_user

from ..models import Tag

class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ('id', 'title', 'created_by')
    extra_kwargs = {
      'created_by': {
        'read_only': True
      },
      'id': {
        'read_only': True
      },
    }

  def create(self, validated_data):
    instance = self.Meta.model(**validated_data)
    instance.created_by = get_user(self.context.get('request'))
    instance.save()
    return instance