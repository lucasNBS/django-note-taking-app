from rest_framework import serializers

from accounts.api.utils import get_user

from .. import utils
from ..models import Folders


class FoldersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folders
        fields = ("id", "title")
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        utils.create_permission_to_folder_user_has_just_created(
            instance, get_user(self.context["request"])
        )
        return instance
