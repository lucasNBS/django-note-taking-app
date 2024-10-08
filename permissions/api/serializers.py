from rest_framework import serializers
from ..models import Permission
from ..choices import AllowToCreatePermissionType

class PermissionSerializer(serializers.ModelSerializer):
  type = serializers.ChoiceField(choices=AllowToCreatePermissionType, allow_blank=False)

  class Meta:
    model = Permission
    fields = '__all__'
    extra_kwargs = {
      'id': {
        'read_only': True
      }
    }
