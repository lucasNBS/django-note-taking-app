from rest_framework.response import Response
from rest_framework import viewsets, parsers, exceptions
from accounts.api.permissions import IsAuthenticated
from accounts.api.utils import get_user

from .permissions import IsCreator
from .serializers import TagSerializer
from ..models import Tag

class TagView(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  permission_classes = (IsAuthenticated, IsCreator)

  def list(self, request):
    user = get_user(request)
    queryset = Tag.objects.filter(created_by=user)
    serializer = TagSerializer(queryset, many=True)
    return Response(serializer.data)
