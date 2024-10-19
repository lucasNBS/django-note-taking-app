from rest_framework import viewsets
from rest_framework.response import Response

from accounts.api.permissions import IsAuthenticated
from accounts.api.utils import get_user

from ..models import Tag
from .permissions import IsCreator
from .serializers import TagSerializer


class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticated, IsCreator)

    def list(self, request):
        user = get_user(request)
        queryset = Tag.objects.filter(created_by=user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)
