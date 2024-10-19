from django.core.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.response import Response

from accounts.api.permissions import IsAuthenticated
from accounts.api.utils import get_user
from core.choices import DataType
from core.permissions import HasAccessToShareableModelData
from permissions.choices import PermissionType
from permissions.models import Permission

from ..models import Folders
from .serializers import FoldersSerializer


class FoldersView(viewsets.ModelViewSet):
    queryset = Folders.objects.all()
    serializer_class = FoldersSerializer
    permission_classes = (IsAuthenticated, HasAccessToShareableModelData)

    def list(self, request):
        user = get_user(request)
        permissions_ids_of_folders_user_has_access = Permission.objects.filter(
            user=user, data__type=DataType.FOLDER
        ).values_list("data__id", flat=True)
        queryset = Folders.objects.filter(id__in=permissions_ids_of_folders_user_has_access)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FoldersSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        obj = self.get_object()

        permission = Permission.objects.filter(
            user=request.user,
            data__id=obj.id,
            data__type=DataType.FOLDER,
        ).exclude(type=PermissionType.READER)

        if not permission.exists():
            raise PermissionDenied("You cannot perform this action")

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()

        permission = Permission.objects.filter(
            user=request.user,
            data__id=obj.id,
            data__type=DataType.FOLDER,
            type=PermissionType.CREATOR,
        )

        if not permission.exists():
            raise PermissionDenied("You cannot perform this action")

        permission.first().delete()
        obj.delete()

        return Response(status=204)
