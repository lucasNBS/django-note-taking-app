import re

from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from core.choices import DataType
from permissions.choices import PermissionType
from permissions.models import Permission

from .forms import FolderForm
from .models import Folders


def include_general_folder_in_queryset(folders):
    general_folder = Folders.objects.filter(title="General").first()
    folders = folders.union(Folders.objects.filter(id=general_folder.id))
    return folders


# Create your views here.
class CreateFolder(CreateView):
    model = Folders
    template_name = "folders/form.html"
    form_class = FolderForm
    success_url = reverse_lazy("notes-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["creator"] = self.request.user
        return kwargs


class UpdateFolder(UpdateView):
    model = Folders
    template_name = "folders/form.html"
    form_class = FolderForm
    success_url = reverse_lazy("notes-list")
    pk_url_kwarg = "id"

    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)

        permission = (
            Permission.objects.filter(
                user=self.request.user,
                data__id=obj.id,
                data__type=DataType.FOLDER,
            )
            .exclude(type=PermissionType.READER)
            .exists()
        )

        if not permission:
            raise PermissionDenied("You cannot perform this action")

        return obj


class DeleteFolder(DeleteView):
    model = Folders
    template_name = "folders/confirm_delete.html"
    success_url = reverse_lazy("notes-list")
    pk_url_kwarg = "id"

    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)

        permission = Permission.objects.filter(
            user=self.request.user,
            data__id=obj.id,
            data__type=DataType.FOLDER,
            type=PermissionType.CREATOR,
        )

        if not permission.exists():
            raise PermissionDenied("You cannot perform this action")

        permission.first().delete()

        return obj


def autocomplete_folder_view(request):
    search = request.GET.get("search")
    limit = 20

    folders_user_has_access_ids = (
        Permission.objects.filter(user=request.user, data__type=DataType.FOLDER)
        .filter(Q(type=PermissionType.CREATOR) | Q(type=PermissionType.EDITOR))
        .filter(Q(data__title__icontains=search) | Q(data__title__startswith=search))
        .values_list("data__id", flat=True)
    )

    folders_user_has_access_as_creator_or_reader = Folders.objects.filter(
        id__in=folders_user_has_access_ids
    )

    if re.match(search, "General", re.I):
        folders_user_has_access_as_creator_or_reader = include_general_folder_in_queryset(
            folders_user_has_access_as_creator_or_reader
        )

    response = [
        {"title": folder.title, "id": folder.id}
        for folder in folders_user_has_access_as_creator_or_reader
    ][:limit]

    return JsonResponse(response, safe=False)
