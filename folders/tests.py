from django.urls import reverse
from django.contrib import auth
from django.test import TestCase, RequestFactory, Client

from accounts import utils
from permissions.models import Permission
from permissions.choices import PermissionType

from . import models, views

# Create your tests here.
class FoldersOperationsTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client = Client()
    user = utils.create_default_user()
    utils.log_in_default_user(self.client)
    self.client_user = auth.get_user(self.client)
    self.folder = models.Folders.objects.create(title="Folder 1")
    Permission.objects.create(data=self.folder, user=self.client_user, type=PermissionType.CREATOR)

  def test_create_folder(self):
    folder_data = {'title': 'Folder 2'}

    request = RequestFactory().post("/", folder_data)
    request.user = self.client_user

    views.CreateFolder.as_view()(request)
    folder_exists = models.Folders.objects.filter(title="Folder 2").exists()
    self.assertTrue(folder_exists)

  def test_update_folder(self):
    folder_new_data = {'title': 'Folder 1 New Title'}
    request = RequestFactory().post("/", folder_new_data)
    request.user = self.client_user

    views.UpdateFolder.as_view()(request, id=self.folder.id)
    folder_exists = models.Folders.objects.filter(title="Folder 1 New Title").exists()
    self.assertTrue(folder_exists)

  def test_delete_folder(self):
    request = RequestFactory().post("/")
    request.user = self.client_user

    views.DeleteFolder.as_view()(request, id=self.folder.id)
    folder_exists = models.Folders.objects.filter(title="Folder 1").exists()
    self.assertFalse(folder_exists)


class FoldersValidationTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client = Client()
    user = utils.create_default_user()
    utils.log_in_default_user(self.client)
    self.client_user = auth.get_user(self.client)
    self.folder = models.Folders.objects.create(title="Folder 1")

  def setUp(self):
    utils.log_in_default_user(self.client)

  def test_editor_should_update_folder(self):
    Permission.objects.create(data=self.folder, user=self.client_user, type=PermissionType.EDITOR)

    folder_new_data = {'title': 'Folder 1 New Title'}

    kwargs = {'id': self.folder.id}
    url = reverse('folders-update', kwargs=kwargs)
    response = self.client.post(url, folder_new_data)

    updated_folder_exists = models.Folders.objects.filter(title="Folder 1 New Title").exists()
    self.assertTrue(updated_folder_exists)

  def test_editor_should_not_delete_folder(self):
    Permission.objects.create(data=self.folder, user=self.client_user, type=PermissionType.EDITOR)

    kwargs = {'id': self.folder.id}
    url = reverse('folders-delete', kwargs=kwargs)
    response = self.client.post(url)

    deleted_folder_still_exists = models.Folders.objects.filter(title="Folder 1").exists()
    
    self.assertTrue(deleted_folder_still_exists)
    self.assertEqual(response.status_code, 403)

  def test_reader_should_not_update_folder(self):
    Permission.objects.create(data=self.folder, user=self.client_user, type=PermissionType.READER)

    folder_new_data = {'title': 'Folder 1 New Title'}

    kwargs = {'id': self.folder.id}
    url = reverse('folders-update', kwargs=kwargs)
    response = self.client.post(url, folder_new_data)

    updated_folder_exists = models.Folders.objects.filter(title="Folder 1 New Title").exists()
    
    self.assertFalse(updated_folder_exists)
    self.assertEqual(response.status_code, 403)

  def test_reader_should_not_delete_folder(self):
    Permission.objects.create(data=self.folder, user=self.client_user, type=PermissionType.READER)

    kwargs = {'id': self.folder.id}
    url = reverse('folders-delete', kwargs=kwargs)
    response = self.client.post(url)

    deleted_folder_still_exists = models.Folders.objects.filter(title="Folder 1").exists()
    
    self.assertTrue(deleted_folder_still_exists)
    self.assertEqual(response.status_code, 403)

  def test_user_without_permission_should_not_update_folder(self):
    folder_new_data = {'title': 'Folder 1 New Title'}

    kwargs = {'id': self.folder.id}
    url = reverse('folders-update', kwargs=kwargs)
    response = self.client.post(url, folder_new_data)

    updated_folder_exists = models.Folders.objects.filter(title="Folder 1 New Title").exists()
    
    self.assertFalse(updated_folder_exists)
    self.assertEqual(response.status_code, 403)

  def test_user_without_permission_should_not_delete_folder(self):
    kwargs = {'id': self.folder.id}
    url = reverse('folders-delete', kwargs=kwargs)
    response = self.client.post(url)

    deleted_folder_still_exists = models.Folders.objects.filter(title="Folder 1").exists()
    
    self.assertTrue(deleted_folder_still_exists)
    self.assertEqual(response.status_code, 403)

class FoldersAutocompleteTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client = Client()
    user = utils.create_default_user()
    utils.log_in_default_user(self.client)
    self.client_user = auth.get_user(self.client)
    self.folder = models.Folders.objects.create(title="Folder 1")
    Permission.objects.create(data=self.folder, user=self.client_user, type=PermissionType.CREATOR)

  def test_autocomplete_list_general_folder(self):
    search_data = {'search': 'General'}
    general_folder = models.Folders.objects.filter(title="General").first()

    request = RequestFactory().get("/", search_data)
    request.user = self.client_user

    response = views.autocomplete_folder_view(request)

    self.assertJSONEqual(response.content, [{"title": "General", "id": general_folder.id}])

  def test_autocomplete_list_created_folder(self):
    search_data = {'search': 'Folder'}
    request = RequestFactory().get("/", search_data)
    request.user = self.client_user

    response = views.autocomplete_folder_view(request)

    self.assertJSONEqual(response.content, [{"title": "Folder 1", "id": self.folder.id}])

  def test_autocomplete_list_shared_folder(self):
    folder = models.Folders.objects.create(title="Folder 2")
    Permission.objects.create(data=folder, user=self.client_user, type=PermissionType.EDITOR)

    search_data = {'search': 'Folder 2'}
    request = RequestFactory().get("/", search_data)
    request.user = self.client_user

    response = views.autocomplete_folder_view(request)

    self.assertJSONEqual(response.content, [{"title": "Folder 2", "id": folder.id}])

  def test_autocomplete_not_list_non_shared_folder(self):
    folder = models.Folders.objects.create(title="Folder 2")

    search_data = {'search': 'Folder 2'}
    request = RequestFactory().get("/", search_data)
    request.user = self.client_user

    response = views.autocomplete_folder_view(request)

    self.assertJSONEqual(response.content, [])
