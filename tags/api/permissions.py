from rest_framework import permissions, exceptions
from accounts.api.utils import get_user

class IsCreator(permissions.BasePermission):
  message = "You do not have access to this tag"

  def has_object_permission(self, request, view, obj):
    user = get_user(request)
    return user == obj.created_by
