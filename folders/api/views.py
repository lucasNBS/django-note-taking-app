from rest_framework.response import Response
from rest_framework import viewsets, parsers, exceptions

from accounts.api.permissions import IsAuthenticated
from accounts.api.utils import get_user
from core.choices import DataType
from core.permissions import HasAccess
from permissions.models import Permission

from .serializers import FoldersSerializer
from ..models import Folders

class FoldersView(viewsets.ModelViewSet):
  queryset = Folders.objects.all()
  serializer_class = FoldersSerializer
  permission_classes = (IsAuthenticated, HasAccess)

  def list(self, request):
    user = get_user(request)
    folders_user_has_access_id = Permission.objects.filter(
      user=user, data__type=DataType.FOLDER
    ).values_list("data__id", flat=True)
    queryset = Folders.objects.filter(id__in=folders_user_has_access_id)
    serializer = FoldersSerializer(queryset, many=True)
    return Response(serializer.data)
