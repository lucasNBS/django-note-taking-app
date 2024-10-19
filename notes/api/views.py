from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.api.permissions import IsAuthenticated
from accounts.api.utils import get_user
from core.choices import DataType
from core.permissions import HasAccessToShareableModelData
from permissions.choices import PermissionType
from permissions.models import Permission

from ..models import Like, Note
from .serializers import NoteSerializer


class NotesView(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated, HasAccessToShareableModelData)

    def _get_notes_user_has_access(self, request):
        user = get_user(request)
        notes_user_has_access_ids = Permission.objects.filter(
            user=user, data__type=DataType.NOTE
        ).values_list("data__id", flat=True)
        notes_user_has_access = Note.all_objects.filter(id__in=notes_user_has_access_ids)
        return notes_user_has_access

    def _apply_filters(self, queryset):
        query_params = self.request.query_params

        if query_params.get("title", None):
            queryset = queryset.filter(title__icontains=query_params.get("title"))

        if query_params.get("start-date", None):
            queryset = queryset.filter(created_at__gte=query_params.get("start-date"))

        if query_params.get("end-date", None):
            queryset = queryset.filter(created_at__lte=query_params.get("end-date"))

        if query_params.get("tags", None):
            queryset = queryset.filter(tags__id__in=query_params.get("tags"))

        return queryset

    @action(detail=True, methods=["post"])
    def restore_note(self, request, pk=None):
        permission_exists = Permission.objects.filter(
            user=get_user(request),
            data__type=DataType.NOTE,
            data__note__is_deleted=True,
            data__id=int(pk),
            type=PermissionType.CREATOR,
        ).exists()
        if not permission_exists:
            raise PermissionDenied("You cannot perform this action")

        note = Note.all_objects.filter(is_deleted=True).get(id=int(pk))
        note.restore()
        serializer = self.serializer_class(note)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def starred(self, request, pk=None):
        user = get_user(request)
        notes_user_has_access = self._get_notes_user_has_access(request)

        starred_notes_user_has_access_ids = []
        for note in notes_user_has_access:
            if note.like_set.filter(user=user).exists():
                starred_notes_user_has_access_ids.append(note.id)
        starred_notes_user_has_access = notes_user_has_access.filter(
            id__in=starred_notes_user_has_access_ids, is_deleted=False
        )

        queryset = self._apply_filters(starred_notes_user_has_access)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def trash(self, request, pk=None):
        notes_user_has_access = self._get_notes_user_has_access(request)
        deleted_notes_user_has_access = notes_user_has_access.filter(is_deleted=True)
        queryset = self._apply_filters(deleted_notes_user_has_access)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def folder(self, request, pk=None):
        user = get_user(request)

        folder_permission = Permission.objects.filter(
            user=user, data__id=int(pk), data__type=DataType.FOLDER
        )

        if not folder_permission.exists():
            raise PermissionDenied("You do not have access to this folder")

        notes_user_has_access = self._get_notes_user_has_access(request)
        folder_notes = notes_user_has_access.filter(folder__id=int(pk))
        queryset = self._apply_filters(folder_notes)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def shared(self, request, pk=None):
        user = get_user(request)
        notes_user_has_access = self._get_notes_user_has_access(request)

        shared_notes_user_has_access_ids = []
        for note in notes_user_has_access:
            if (
                note.permission_set.filter(user=user)
                .filter(Q(type=PermissionType.READER) | Q(type=PermissionType.EDITOR))
                .exists()
            ):
                shared_notes_user_has_access_ids.append(note.id)
        shared_notes_user_has_access = notes_user_has_access.filter(
            id__in=shared_notes_user_has_access_ids
        )

        queryset = self._apply_filters(shared_notes_user_has_access)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def favorite(self, request, pk=None):
        user = get_user(request)
        note = Note.objects.get(id=pk)

        like_instance = Like.objects.filter(user=user, note=note)
        if like_instance.exists():
            like_instance.first().delete()
        else:
            Like.objects.create(user=user, note=note)

        serializer = self.serializer_class(note)
        return Response(serializer.data)

    def list(self, request):
        notes_user_has_access = self._get_notes_user_has_access(request)
        queryset = self._apply_filters(notes_user_has_access)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        response = super().create(request)
        return response

    def update(self, request, *args, **kwargs):
        obj = self.get_object()

        permission = Permission.objects.filter(
            user=request.user,
            data__id=obj.id,
        ).exclude(type=PermissionType.READER)

        if not permission.exists():
            raise PermissionDenied("You cannot perform this action")

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()

        permission = Permission.objects.filter(
            user=request.user,
            data__id=obj.id,
            data__type=DataType.NOTE,
            type=PermissionType.CREATOR,
        )

        if not permission.exists():
            raise PermissionDenied("You cannot perform this action")

        permission.first().delete()
        obj.delete()

        return Response(status=204)
