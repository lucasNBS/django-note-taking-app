from rest_framework import permissions, exceptions
from accounts.api.utils import get_user
from core.models import ShareableModel
from core.choices import DataType
from folders.models import Folders
from permissions import models, choices

class BaseAccess(permissions.BasePermission):
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
    'OPTIONS': {
      choices.PermissionType.READER: True,
      choices.PermissionType.EDITOR: True,
      choices.PermissionType.CREATOR: True,
    },
  }

  def _can_perform_action(self, request, permission):
    if not self.permissions_relation[request.method][permission.type]:
      raise exceptions.PermissionDenied("You cannot perform this action")
    return True

class HasAccessToShareableModelData(BaseAccess):

  def has_object_permission(self, request, view, obj):
    user = get_user(request)
    permission = models.Permission.objects.filter(user=user, data=obj).first()

    if not permission:
      return False

    self._can_perform_action(request, permission)

    return True

class IsCreatorOfShareableModelData(BaseAccess):

  def has_object_permission(self, request, view, obj):
    user = get_user(request)
    permission = models.Permission.objects.filter(
      user=user, data=obj.data, type=choices.PermissionType.CREATOR
    ).first()

    if not permission:
      return False

    self._can_perform_action(request, permission)

    return True

  def has_permission(self, request, view):
    user = get_user(request)

    try:
      obj = ShareableModel.objects.get(id=view.kwargs['pk'])
    except ShareableModel.DoesNotExist:
      raise exceptions.NotFound()

    permission = models.Permission.objects.filter(
      user=user, data=obj, type=choices.PermissionType.CREATOR
    ).first()

    if not permission:
      return False

    self._can_perform_action(request, permission)

    return True

class HasAccessToPermissions(BaseAccess):

  def has_object_permission(self, request, view, obj):
    user = get_user(request)
    permission = models.Permission.objects.filter(
      user=user, data=obj.data, type=choices.PermissionType.CREATOR
    ).first()

    if not permission:
      return False

    self._can_perform_action(request, permission)

    return True
  
  def has_permission(self, request, view):
    user = get_user(request)

    try:
      object_permission = models.Permission.objects.get(id=view.kwargs['pk'])
    except ShareableModel.DoesNotExist:
      raise exceptions.NotFound()

    permission = models.Permission.objects.filter(
      user=user, data=object_permission.data, type=choices.PermissionType.CREATOR
    ).first()

    if not permission:
      return False

    self._can_perform_action(request, permission)

    return True