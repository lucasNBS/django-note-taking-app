from rest_framework import permissions, exceptions
from accounts.api.utils import get_user
from permissions import models, choices

class HasAccess(permissions.BasePermission):
  message = "You do not have permission to access this data"
  permissions_relation = {
    'GET': {
      choices.PermissionType.READER: True,
      choices.PermissionType.EDITOR: True,
      choices.PermissionType.CREATOR: True,
    },
    'PUT': {
      choices.PermissionType.READER: False,
      choices.PermissionType.EDITOR: True,
      choices.PermissionType.CREATOR: True,
    },
    'POST': {
      choices.PermissionType.READER: True,
      choices.PermissionType.EDITOR: True,
      choices.PermissionType.CREATOR: True,
    },
    'PATCH': {
      choices.PermissionType.READER: False,
      choices.PermissionType.EDITOR: True,
      choices.PermissionType.CREATOR: True,
    },
    'DELETE': {
      choices.PermissionType.READER: False,
      choices.PermissionType.EDITOR: False,
      choices.PermissionType.CREATOR: True,
    },
  }

  def has_object_permission(self, request, view, obj):
    user = get_user(request)
    permission = models.Permission.objects.filter(user=user, data=obj).first()

    if not permission:
      return False

    self.can_perform_action(request, permission)

    return True

  def can_perform_action(self, request, permission):
    if not self.permissions_relation[request.method][permission.type]:
      raise exceptions.PermissionDenied("You cannot perform this action")
    return True