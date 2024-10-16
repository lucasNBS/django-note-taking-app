from rest_framework.test import APITestCase, APIRequestFactory

from accounts import utils
from accounts.api.utils import get_user
from permissions.models import Permission
from permissions.choices import PermissionType
from folders.models import Folders
from notes.models import Note
from notes import views as notes_views

from . import views
from .. import models

def create_folder_permission_to_user_to_share_data(self):
  share_data = {
    'user': self.user_to_share_data_with.id,
    'type': PermissionType.READER,
    'data': self.folder.id,
  }

  request = APIRequestFactory().post("/", share_data)
  request.user = self.user

  views.FolderPermissionsView.as_view()(request, pk=self.folder.id)

# Create your tests here.
class PermissionOperationsAPITestCase(APITestCase):
  @classmethod
  def setUpTestData(self):
    self.user = utils.create_default_user()
    
    self.folder = Folders.objects.create(title="Folder 1")
    self.permission = Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.CREATOR
    )

    self.user_to_share_data_with = utils.create_user(
      username='teste',
      email='teste@email.com',
      password='teste',
    )
    self.user_to_share_data_permission = models.Permission.objects.create(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=PermissionType.READER
    )

  def test_api_list_permissions(self):
    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.FolderPermissionsView.as_view()(request, pk=self.folder.id)
    response.render()

    self.assertIn(str(self.user_to_share_data_permission.type), str(response.content))

  def test_api_detail_permissions(self):
    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_permission.id
    )
    response.render()

    self.assertIn(str(self.user_to_share_data_permission.type), str(response.content))

  def test_api_create_permission(self):
    share_data = {
      'user': self.user_to_share_data_with.id,
      'type': PermissionType.READER,
      'data': self.folder.id,
    }

    request = APIRequestFactory().post("/", share_data)
    request.user = self.user

    response = views.FolderPermissionsView.as_view()(request, pk=self.folder.id)
    permission_exists = models.Permission.objects.filter(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=PermissionType.READER,
    ).exists()
    self.assertTrue(permission_exists)

  def test_api_update_permission(self):
    share_data = {
      'user': self.user_to_share_data_with.id,
      'type': PermissionType.EDITOR,
      'data': self.folder.id,
    }

    request = APIRequestFactory().patch("/", share_data)
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_permission.id
    )

    permission_exists = models.Permission.objects.filter(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=PermissionType.EDITOR,
    ).exists()
    self.assertTrue(permission_exists)

  def test_api_delete_permission(self):
    request = APIRequestFactory().delete("/")
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_permission.id
    )

    permission_exists = models.Permission.objects.filter(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=self.user_to_share_data_permission.type,
    ).exists()
    self.assertFalse(permission_exists)

class FolderPermissionsAPITestCase(APITestCase):
  @classmethod
  def setUpTestData(self):
    self.user = utils.create_default_user()

    self.folder = Folders.objects.create(title="Folder 1")
    self.permission = models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.CREATOR
    )

    self.note = Note.objects.create(
      title="Note 1",
      description="Note 1 description",
      content="Note 1 content",
      folder=self.folder,
    )
    note_permission = models.Permission.objects.create(
      data=self.note, user=self.user, type=PermissionType.CREATOR
    )

    self.user_to_share_data_with = utils.create_user(
      username='teste',
      email='teste@email.com',
      password='teste',
    )

  def test_api_create_notes_permission_when_sharing_folder(self):
    create_folder_permission_to_user_to_share_data(self)
    permission_exists = models.Permission.objects.filter(
      data=self.note,
      user=self.user_to_share_data_with,
      type=PermissionType.READER,
    ).exists()

    self.assertTrue(permission_exists)

  def test_api_update_notes_permission_when_updating_shared_folder(self):
    create_folder_permission_to_user_to_share_data(self)
    folder_permission = models.Permission.objects.get(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=PermissionType.READER,
    )

    update_data = {
      'user': self.user_to_share_data_with.id,
      'type': PermissionType.READER,
      'data': self.folder.id,
    }

    request = APIRequestFactory().patch("/", update_data)
    request.user = self.user

    views.DetailFolderPermissionView.as_view()(request, pk=folder_permission.id)

    note_permission_exists = models.Permission.objects.filter(
      data=self.note,
      user=self.user_to_share_data_with,
      type=PermissionType.EDITOR,
    ).exists()

    self.assertTrue(note_permission_exists)

  def test_api_delete_notes_permission_when_deleting_shared_folder(self):
    create_folder_permission_to_user_to_share_data(self)
    folder_permission = models.Permission.objects.get(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=PermissionType.READER,
    )

    request = APIRequestFactory().delete("/")
    request.user = self.user

    views.DetailFolderPermissionView.as_view()(request, pk=folder_permission.id)

    note_permission_exists = models.Permission.objects.filter(
      data=self.note,
      user=self.user_to_share_data_with,
      type=PermissionType.READER,
    ).exists()

    self.assertFalse(note_permission_exists)

  def test_api_create_note_permission_for_shared_folder_after_sharing_it(self):
    create_folder_permission_to_user_to_share_data(self)

    new_note = Note.objects.create(
      title="Note 2",
      description="Note 2 description",
      content="Note 2 content",
      folder=self.folder,
    )

    new_permission_exists = models.Permission.objects.filter(
      data=new_note,
      user=self.user_to_share_data_with,
      type=PermissionType.READER,
    ).exists()

    self.assertTrue(new_permission_exists)

  def test_api_alter_note_permission_in_shared_folder_when_changing_folder(self):
    create_folder_permission_to_user_to_share_data(self)

    new_folder = Folders.objects.create(title="Folder 2")
    new_permission = models.Permission.objects.create(
      data=new_folder, user=self.user, type=PermissionType.CREATOR
    )

    new_folder_permission_data = {
      'user': self.user_to_share_data_with.id,
      'type': PermissionType.EDITOR,
      'data': new_folder.id,
    }

    request = APIRequestFactory().post("/", new_folder_permission_data)
    request.user = self.user

    views.FolderPermissionsView.as_view()(request, pk=new_folder.id)

    update_note_data = {
      'title': self.note.title,
      'description': self.note.description,
      'content': self.note.content,
      'folder': new_folder.id,
    }

    update_note_request = APIRequestFactory().post("/", update_note_data)
    update_note_request.user = self.user

    notes_views.UpdateNoteView.as_view()(update_note_request, id=self.note.id)

    previous_note_permission_exists = models.Permission.objects.filter(
      data=self.note,
      user=self.user_to_share_data_with,
      type=PermissionType.READER,
    ).exists()

    new_note_permission_exists = models.Permission.objects.filter(
      data=self.note,
      user=self.user_to_share_data_with,
      type=PermissionType.EDITOR,
    ).exists()

    self.assertFalse(previous_note_permission_exists)
    self.assertTrue(new_note_permission_exists)

class PermissionsValidationTestCase(APITestCase):
  @classmethod
  def setUpTestData(self):
    self.user = utils.create_default_user()
    self.folder = Folders.objects.create(title="Folder 1")

    self.user_to_share_data_with = utils.create_user(
      username='teste',
      email='teste@email.com',
      password='teste',
    )
    self.user_to_share_data_with_permission = models.Permission.objects.create(
      data=self.folder, user=self.user_to_share_data_with, type=PermissionType.EDITOR
    )

  def setUp(self):
    utils.log_in_default_user(self.client)

  def test_api_editor_user_should_not_list_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.EDITOR
    )

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.FolderPermissionsView.as_view()(request, pk=self.folder.id)
    response.render()

    self.assertNotIn(f"{self.folder}", str(response.content))
    self.assertEqual(response.status_code, 403)

  def test_api_editor_user_should_not_detail_permission(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.EDITOR
    )

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_with_permission.id
    )
    response.render()

    self.assertNotIn(f"{self.user_to_share_data_with_permission.id}", str(response.content))
    self.assertEqual(response.status_code, 403)

  def test_api_editor_user_should_not_create_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.EDITOR
    )

    share_data = {
      'user': self.user_to_share_data_with.id,
      'type': PermissionType.READER,
      'data': self.folder.id,
    }

    request = APIRequestFactory().post("/", share_data)
    request.user = self.user

    response = views.FolderPermissionsView.as_view()(request, pk=self.folder.id)

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with,
      type=PermissionType.READER,
      data=self.folder.id,
    ).exists()
    self.assertFalse(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_editor_user_should_not_update_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.EDITOR
    )

    share_data = {
      'user': self.user_to_share_data_with.id,
      'type': PermissionType.READER,
      'data': self.folder.id,
    }

    request = APIRequestFactory().patch("/", share_data)
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_with_permission.id
    )

    permission_exists = models.Permission.objects.filter(
      user=self.user,
      type=PermissionType.READER,
      data=self.folder,
    ).exists()

    self.assertFalse(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_editor_user_should_not_delete_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.EDITOR
    )

    request = APIRequestFactory().delete("/")
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_with_permission.id
    )

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with_permission.user,
      type=self.user_to_share_data_with_permission.type,
      data=self.user_to_share_data_with_permission.data,
    ).exists()

    self.assertTrue(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_reader_user_should_not_list_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.READER
    )

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.FolderPermissionsView.as_view()(request, pk=self.folder.id)
    response.render()

    self.assertNotIn(f'{self.folder}', str(response.content))
    self.assertEqual(response.status_code, 403)

  def test_api_reader_user_should_not_detail_permission(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.READER
    )

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_with_permission.id
    )
    response.render()

    self.assertNotIn(f"{self.user_to_share_data_with_permission.id}", str(response.content))
    self.assertEqual(response.status_code, 403)

  def test_api_reader_user_should_not_create_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.READER
    )

    share_data = {
      'user': self.user_to_share_data_with.id,
      'type': PermissionType.READER,
      'data': self.folder.id,
    }

    request = APIRequestFactory().post("/", share_data)
    request.user = self.user

    response = views.FolderPermissionsView.as_view()(request, pk=self.folder.id)

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with,
      type=PermissionType.READER,
      data=self.folder.id,
    ).exists()
    self.assertFalse(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_reader_user_should_not_update_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.READER
    )

    share_data = {
      'user': self.user_to_share_data_with.id,
      'type': PermissionType.READER,
      'data': self.folder.id,
    }

    request = APIRequestFactory().patch("/", share_data)
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_with_permission.id
    )

    permission = models.Permission.objects.get(id=self.user_to_share_data_with_permission.id)

    self.assertTrue(permission.type == self.user_to_share_data_with_permission.type)
    self.assertEqual(response.status_code, 403)

  def test_api_reader_user_should_not_delete_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=PermissionType.READER
    )

    request = APIRequestFactory().delete("/")
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_with_permission.id
    )

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with_permission.user,
      type=self.user_to_share_data_with_permission.type,
      data=self.user_to_share_data_with_permission.data,
    ).exists()

    self.assertTrue(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_user_without_permission_should_not_list_permissions(self):
    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.FolderPermissionsView.as_view()(request, pk=self.folder.id)
    response.render()

    self.assertNotIn(f'{self.folder}', str(response.content))
    self.assertEqual(response.status_code, 403)

  def test_api_user_without_permission_should_not_detail_permissions(self):
    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_with_permission.id
    )
    response.render()

    self.assertNotIn(f"{self.user_to_share_data_with_permission.id}", str(response.content))
    self.assertEqual(response.status_code, 403)

  def test_api_user_without_permission_should_not_create_permissions(self):
    share_data = {
      'user': self.user_to_share_data_with,
      'type': PermissionType.READER,
      'data': self.folder.id,
    }

    request = APIRequestFactory().post("/", share_data)
    request.user = self.user

    response = views.FolderPermissionsView.as_view()(request, pk=self.folder.id)
    response.render()

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with,
      type=PermissionType.READER,
      data=self.folder.id,
    ).exists()

    self.assertFalse(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_user_without_permission_should_not_update_permissions(self):
    share_data = {
      'user': self.user_to_share_data_with.id,
      'type': PermissionType.READER,
      'data': self.folder.id,
    }

    request = APIRequestFactory().patch("/", share_data)
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_with_permission.id
    )

    permission_exists = models.Permission.objects.filter(
      user=self.user,
      type=PermissionType.READER,
      data=self.folder,
    ).exists()

    self.assertFalse(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_user_without_permission_should_not_delete_permissions(self):
    request = APIRequestFactory().delete("/")
    request.user = self.user

    response = views.DetailFolderPermissionView.as_view()(
      request, pk=self.user_to_share_data_with_permission.id
    )

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with_permission.user,
      type=self.user_to_share_data_with_permission.type,
      data=self.user_to_share_data_with_permission.data,
    ).exists()

    self.assertTrue(permission_exists)
    self.assertEqual(response.status_code, 403)
