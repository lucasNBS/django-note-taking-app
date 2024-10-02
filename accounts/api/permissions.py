from rest_framework import permissions
from .utils import get_user

class IsAuthenticated(permissions.BasePermission):

  def has_permission(self, request, view):
    try:
      user = get_user(request)
      return user is not None
    except:
      return False

  def has_object_permission(self, request, view, obj):
    try:
      user = get_user(request)
      return user is not None
    except:
      return False