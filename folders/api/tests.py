from rest_framework.test import APIClient, APITestCase, APIRequestFactory

from accounts import utils
from accounts.api.utils import get_user
from permissions.models import Permission
from permissions.choices import PermissionType

from . import views
from .. import models

# Create your tests here.
class FolderOperationsAPITestCase(APITestCase):
  @classmethod
  def setUpTestData(self):
    self.client = APIClient()
    self.user = utils.create_default_user()
    self.folder = models.Folders.objects.create(title="Folder 1")
    Permission.objects.create(data=self.folder, user=self.user, type=PermissionType.CREATOR)

  def setUp(self):
    utils.log_in_default_user(self.client)

  def test_api_create_folder(self):
    folder_data = {
      'title': 'Folder 2'
    }

    request = APIRequestFactory().post("/", folder_data)
    request.user = self.user

    views.FoldersView.as_view({'post': 'create'})(request)
    folder_exists = models.Folders.objects.filter(title="Folder 2").exists()
    self.assertTrue(folder_exists)

  def test_api_update_folder(self):
    folder_new_data = {
      'title': 'Folder 1 New Title'
    }

    request = APIRequestFactory().post("/", folder_new_data)
    request.user = self.user

    views.FoldersView.as_view({'post': 'update'})(request, pk=self.folder.id)
    folder_exists = models.Folders.objects.filter(title="Folder 1 New Title").exists()
    self.assertTrue(folder_exists)

  def test_api_delete_folder(self):
    request = APIRequestFactory().post("/")
    request.user = self.user

    views.FoldersView.as_view({'post': 'destroy'})(request, pk=self.folder.id)
    folder_still_exists = models.Folders.objects.filter(title="Folder 1").exists()
    self.assertFalse(folder_still_exists)

class FoldersValidationAPITestCase(APITestCase):
  @classmethod
  def setUpTestData(self):
    self.client = APIClient()
    self.user = utils.create_default_user()
    self.folder = models.Folders.objects.create(title="Folder 1")

  def setUp(self):
    utils.log_in_default_user(self.client)

  def test_api_editor_should_update_folder(self):
    Permission.objects.create(data=self.folder, user=self.user, type=PermissionType.EDITOR)

    folder_new_data = {
      'title': 'Folder 1 New Title'
    }

    request = APIRequestFactory().post("/", folder_new_data)
    request.user = self.user

    views.FoldersView.as_view({'post': 'update'})(request, pk=self.folder.id)
    updated_folder_exists = models.Folders.objects.filter(title="Folder 1 New Title").exists()
    self.assertTrue(updated_folder_exists)

  def test_api_editor_should_not_delete_folder(self):
    Permission.objects.create(data=self.folder, user=self.user, type=PermissionType.EDITOR)

    request = APIRequestFactory().post("/")
    request.user = self.user

    response = views.FoldersView.as_view({'post': 'destroy'})(request, pk=self.folder.id)

    deleted_folder_still_exists = models.Folders.objects.filter(title="Folder 1").exists()
    self.assertTrue(deleted_folder_still_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_reader_should_not_update_folder(self):
    Permission.objects.create(data=self.folder, user=self.user, type=PermissionType.READER)

    folder_new_data = {'title': 'Folder 1 New Title'}

    request = APIRequestFactory().post("/", folder_new_data)
    request.user = self.user

    response = views.FoldersView.as_view({'post': 'update'})(request, pk=self.folder.id)
    updated_folder_exists = models.Folders.objects.filter(title="Folder 1 New Title").exists()

    self.assertFalse(updated_folder_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_reader_should_not_delete_folder(self):
    Permission.objects.create(data=self.folder, user=self.user, type=PermissionType.READER)

    request = APIRequestFactory().post("/")
    request.user = self.user

    response = views.FoldersView.as_view({'post': 'destroy'})(request, pk=self.folder.id)
    deleted_folder_still_exists = models.Folders.objects.filter(title="Folder 1").exists()
    
    self.assertTrue(deleted_folder_still_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_user_without_permission_should_not_update_folder(self):
    folder_new_data = {'title': 'Folder 1 New Title'}

    request = APIRequestFactory().post("/", folder_new_data)
    request.user = self.user

    response = views.FoldersView.as_view({'post': 'update'})(request, pk=self.folder.id)
    updated_folder_exists = models.Folders.objects.filter(title="Folder 1 New Title").exists()
    
    self.assertFalse(updated_folder_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_user_without_permission_should_not_delete_folder(self):
    request = APIRequestFactory().post("/")
    request.user = self.user

    response = views.FoldersView.as_view({'post': 'destroy'})(request, pk=self.folder.id)
    deleted_folder_still_exists = models.Folders.objects.filter(title="Folder 1").exists()
    
    self.assertTrue(deleted_folder_still_exists)
    self.assertEqual(response.status_code, 403)
