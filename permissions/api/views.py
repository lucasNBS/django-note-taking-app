from rest_framework.response import Response
from rest_framework import viewsets, parsers, generics, exceptions, mixins

from accounts.api.permissions import IsAuthenticated
from accounts.api.utils import get_user
from accounts.models import User
from core.choices import DataType
from core.permissions import IsCreatorOfShareableModelData, HasAccessToPermissions
from core.models import ShareableModel
from notes.models import Note
from folders.models import Folders

from .. import constants
from .serializers import PermissionSerializer
from ..choices import PermissionType
from ..models import Permission


class ListDataPermissionsView(mixins.RetrieveModelMixin, generics.GenericAPIView):
  serializer_class = PermissionSerializer
  permission_classes = (IsAuthenticated, IsCreatorOfShareableModelData)

  def _get_data(self, pk):
    try:
      return self.queryset.get(id=pk)
    except self.queryset.model.DoesNotExist:
      raise exceptions.NotFound()

  def retrieve(self, request, pk=None):
    user = get_user(request)
    data = self._get_data(pk)
    queryset = Permission.objects.filter(data=data)

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.serializer_class(page, many=True)
      return self.get_paginated_response(serializer.data)

    serializer = self.serializer_class(queryset, many=True)
    return Response(serializer.data)

  def get(self, request, pk=None):
    return self.retrieve(request, pk)

class NotePermissionsView(ListDataPermissionsView, mixins.CreateModelMixin):
  queryset = Note.objects.all()

  def create(self, request, pk):
    data = parsers.JSONParser().parse(request)

    data['data'] = pk
    serializer = self.serializer_class(data=data)

    if serializer.is_valid():
      serializer.save()
      if serializer.data['id'] is None:
        raise exceptions.ValidationError({'message': 'The selected user already has permission'})
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def post(self, request, pk=None):
    return self.create(request, pk)

class FolderPermissionsView(ListDataPermissionsView, mixins.CreateModelMixin):
  queryset = Folders.objects.all()

  def _share_folder_notes(self, data):
    folder_notes = self.queryset.get(id=data['data']).note_set.all()
    user = User.objects.get(id=data['user'])

    for note in folder_notes:
      note_permission = Permission.objects.filter(user=user, data=note)

      if note_permission.exists():
        note_permission.update(type=constants.permissions_relation[data['type']])
      else:
        Permission.objects.create(data=note, user=user, type=data['type'])

  def create(self, request, pk):
    data = parsers.JSONParser().parse(request)

    data['data'] = pk
    serializer = self.serializer_class(data=data)

    if serializer.is_valid():
      self._share_folder_notes(data)
      serializer.save()
      if serializer.data['id'] is None:
        raise exceptions.ValidationError({'message': 'The selected user already has permission'})
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def post(self, request, pk=None):
    return self.create(request, pk)

class DetailDataPermissionView(mixins.RetrieveModelMixin, generics.GenericAPIView):
  serializer_class = PermissionSerializer
  permission_classes = (IsAuthenticated, HasAccessToPermissions)

  def _get_permission(self, pk):
    try:
      return self.queryset.get(id=pk)
    except Permission.DoesNotExist:
      raise exceptions.NotFound()

  def retrieve(self, request, pk):
    user = get_user(request)
    permission = self._get_permission(pk)
    serializer = self.serializer_class(permission)
    return Response(serializer.data)

  def get(self, request, pk=None):
    return self.retrieve(request, pk)


class DetailNotePermissionView(
  DetailDataPermissionView,
  mixins.UpdateModelMixin,
  mixins.DestroyModelMixin
):
  queryset = Permission.objects.filter(data__type=DataType.NOTE)

  def update(self, request, pk):
    data = parsers.JSONParser().parse(request)
    permission = self._get_permission(pk)

    if permission.type == PermissionType.CREATOR:
      raise exceptions.ValidationError(
        {"message": "Cannot edit CREATOR permission"}
      )

    serializer = self.serializer_class(permission, data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

  def patch(self, request, pk=None):
    return self.update(request, pk)

  def delete(self, request, pk=None):
    permission = self._get_permission(pk)

    if permission.type == PermissionType.CREATOR:
      raise exceptions.ValidationError(
        {"message": "Cannot delete CREATOR permission"}
      )

    return self.destroy(request, pk)

class DetailFolderPermissionView(
  DetailDataPermissionView,
  mixins.UpdateModelMixin,
  mixins.DestroyModelMixin
):
  queryset = Permission.objects.filter(data__type=DataType.FOLDER)

  def _update_shared_folder_notes(self, permission, data):
    user = User.objects.get(id=data['user'])
    folder_notes = Permission.objects.filter(
      user=user,
      data__type=DataType.NOTE,
      type=permission.type,
      data__note__folder=permission.data
    )
    folder_notes.update(type=constants.permissions_relation[permission.type])

  def update(self, request, pk):
    data = parsers.JSONParser().parse(request)
    permission = self._get_permission(pk)

    if permission.type == PermissionType.CREATOR:
      raise exceptions.ValidationError(
        {"message": "Cannot edit CREATOR permission"}
      )

    serializer = self.serializer_class(permission, data=data)
    if serializer.is_valid():
      self._update_shared_folder_notes(permission, data)
      serializer.save()
      return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

  def patch(self, request, pk=None):
    return self.update(request, pk)

  def _delete_shared_folder_notes_permissions(self, permission):
    folder_notes = Permission.objects.filter(
        user=permission.user,
        data__type=DataType.NOTE,
        type=permission.type,
        data__note__folder=permission.data
      )
    for note in folder_notes:
      note.delete()

  def delete(self, request, pk=None):
    permission = self._get_permission(pk)

    if permission.type == PermissionType.CREATOR:
      raise exceptions.ValidationError(
        {"message": "Cannot delete CREATOR permission"}
      )

    response = self.destroy(request, pk)
    self._delete_shared_folder_notes_permissions(permission)
    return response

class ListUserPermissionsView(mixins.ListModelMixin, generics.GenericAPIView):
  queryset = Permission.objects.all()
  serializer_class = PermissionSerializer
  permission_classes = (IsAuthenticated,)

  def retrieve(self, request, pk=None):
    user = get_user(request)
    queryset = Permission.objects.filter(user=user)

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.serializer_class(page, many=True)
      return self.get_paginated_response(serializer.data)
    
    serializer = self.serializer_class(queryset, many=True)
    return Response(serializer.data)

  def get(self, request, pk=None):
    return self.retrieve(request, pk)