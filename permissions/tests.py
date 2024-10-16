from django.urls import reverse
from django.contrib import auth
from django.test import TestCase, RequestFactory, Client

from notes.models import Note
from notes import views as notes_views
from folders.models import Folders
from accounts import utils

from . import models, views, choices, constants

def create_folder_permission_to_user_to_share_data(self):
  share_data = {
    'user': self.user_to_share_data_with,
    'type': choices.PermissionType.READER,
    'data': self.folder.id,
  }

  request = RequestFactory().post("/", share_data)
  request.user = self.client_user

  views.CreatePermissions.as_view()(request, data_id=self.folder.id)


# Create your tests here.
class PermissionsOperationsTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client_user = utils.create_default_user()

    self.folder = Folders.objects.create(title="Folder 1")
    self.permission = models.Permission.objects.create(
      data=self.folder, user=self.client_user, type=choices.PermissionType.CREATOR
    )

    self.user_to_share_data_with = utils.create_user(
      username='teste',
      email='teste@email.com',
      password='teste',
    )
    self.user_to_share_data_permission = models.Permission.objects.create(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=choices.PermissionType.READER
    )

  def test_list_permissions(self):
    request = RequestFactory().get("/")
    request.user = self.client_user

    response = views.ListPermissions.as_view()(request, data_id=self.folder.id)
    response.render()

    self.assertContains(
      response,
      f'<td class="p-2 border-2 border-gray-300">{self.user_to_share_data_permission.type}</td>',
      html="True",
    )
    self.assertNotContains(
      response,
      f'<td class="p-2 border-2 border-gray-300">{choices.PermissionType.CREATOR}</td>',
      html="True",
    )
  
  def test_create_permission(self):
    share_data = {
      'user': self.user_to_share_data_with,
      'type': choices.PermissionType.READER,
      'data': self.folder.id,
    }

    request = RequestFactory().post("/", share_data)
    request.user = self.client_user

    views.CreatePermissions.as_view()(request, data_id=self.folder.id)

    permission_exists = models.Permission.objects.filter(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=choices.PermissionType.READER,
    ).exists()

    self.assertTrue(permission_exists)

  def test_update_permission(self):
    share_data = {'type': self.user_to_share_data_permission.type}

    request = RequestFactory().post("/", share_data)
    request.user = self.client_user

    views.UpdatePermissions.as_view()(
      request, data_id=self.folder.id, id=self.user_to_share_data_permission.id
    )

    permission_exists = models.Permission.objects.filter(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=constants.permissions_relation[self.user_to_share_data_permission.type],
    ).exists()

    self.assertTrue(permission_exists)

  def test_delete_permission(self):
    request = RequestFactory().post("/")
    request.user = self.client_user

    views.DeletePermissions.as_view()(
      request, data_id=self.folder.id, id=self.user_to_share_data_permission.id
    )

    permission_exists = models.Permission.objects.filter(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=self.user_to_share_data_permission.type,
    ).exists()

    self.assertFalse(permission_exists)

class FolderPermissionsTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client_user = utils.create_default_user()

    self.folder = Folders.objects.create(title="Folder 1")
    self.permission = models.Permission.objects.create(
      data=self.folder, user=self.client_user, type=choices.PermissionType.CREATOR
    )
    self.note = Note.objects.create(
      title="Note 1",
      description="Note 1 description",
      content="Note 1 content",
      folder=self.folder,
    )
    note_permission = models.Permission.objects.create(
      data=self.note, user=self.client_user, type=choices.PermissionType.CREATOR
    )

    self.user_to_share_data_with = utils.create_user(
      username='teste',
      email='teste@email.com',
      password='teste',
    )

  def test_create_notes_permission_when_sharing_folder(self):
    create_folder_permission_to_user_to_share_data(self)
    permission_exists = models.Permission.objects.filter(
      data=self.note,
      user=self.user_to_share_data_with,
      type=choices.PermissionType.READER,
    ).exists()

    self.assertTrue(permission_exists)

  def test_update_notes_permission_when_updating_shared_folder(self):
    create_folder_permission_to_user_to_share_data(self)
    folder_permission = models.Permission.objects.get(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=choices.PermissionType.READER,
    )

    update_data = {
      'type': choices.PermissionType.READER,
    }

    request = RequestFactory().post("/", update_data)
    request.user = self.client_user

    views.UpdatePermissions.as_view()(request, data_id=self.folder.id, id=folder_permission.id)

    note_permission_exists = models.Permission.objects.filter(
      data=self.note,
      user=self.user_to_share_data_with,
      type=choices.PermissionType.EDITOR,
    ).exists()

    self.assertTrue(note_permission_exists)

  def test_delete_notes_permission_when_deleting_shared_folder(self):
    create_folder_permission_to_user_to_share_data(self)
    folder_permission = models.Permission.objects.get(
      data=self.folder,
      user=self.user_to_share_data_with,
      type=choices.PermissionType.READER,
    )

    request = RequestFactory().post("/")
    request.user = self.client_user

    views.DeletePermissions.as_view()(request, data_id=self.folder.id, id=folder_permission.id)

    note_permission_exists = models.Permission.objects.filter(
      data=self.note,
      user=self.user_to_share_data_with,
      type=choices.PermissionType.READER,
    ).exists()

    self.assertFalse(note_permission_exists)

  def test_create_note_permission_for_shared_folder_after_sharing_it(self):
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
      type=choices.PermissionType.READER,
    ).exists()

    self.assertTrue(new_permission_exists)

  def test_alter_note_permission_in_shared_folder_when_changing_folder(self):
    create_folder_permission_to_user_to_share_data(self)

    new_folder = Folders.objects.create(title="Folder 2")
    new_permission = models.Permission.objects.create(
      data=new_folder, user=self.client_user, type=choices.PermissionType.CREATOR
    )

    new_folder_permission_data = {
      'user': self.user_to_share_data_with,
      'type': choices.PermissionType.EDITOR,
      'data': new_folder.id,
    }

    request = RequestFactory().post("/", new_folder_permission_data)
    request.user = self.client_user

    views.CreatePermissions.as_view()(request, data_id=new_folder.id)

    update_note_data = {
      'title': self.note.title,
      'description': self.note.description,
      'content': self.note.content,
      'folder': new_folder.id,
    }

    update_note_request = RequestFactory().post("/", update_note_data)
    update_note_request.user = self.client_user

    notes_views.UpdateNoteView.as_view()(update_note_request, id=self.note.id)

    previous_note_permission_exists = models.Permission.objects.filter(
      data=self.note,
      user=self.user_to_share_data_with,
      type=choices.PermissionType.READER,
    ).exists()

    new_note_permission_exists = models.Permission.objects.filter(
      data=self.note,
      user=self.user_to_share_data_with,
      type=choices.PermissionType.EDITOR,
    ).exists()

    self.assertFalse(previous_note_permission_exists)
    self.assertTrue(new_note_permission_exists)

class PermissionsValidationTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client = Client()
    self.user = utils.create_default_user()
    self.folder = Folders.objects.create(title="Folder 1")

    self.user_to_share_data_with = utils.create_user(
      username='teste',
      email='teste@email.com',
      password='teste',
    )
    self.user_to_share_data_with_permission = models.Permission.objects.create(
      data=self.folder, user=self.user_to_share_data_with, type=choices.PermissionType.EDITOR
    )

  def setUp(self):
    utils.log_in_default_user(self.client)

  def test_editor_user_should_not_list_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=choices.PermissionType.EDITOR
    )

    kwargs = {'data_id': self.folder.id}
    url = reverse('notes-permissions-list', kwargs=kwargs)
    response = self.client.get(url)

    self.assertEqual(response.status_code, 403)

  def test_editor_user_should_not_create_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=choices.PermissionType.EDITOR
    )

    share_data = {
      'user': self.user_to_share_data_with,
      'type': choices.PermissionType.READER,
      'data': self.folder.id,
    }

    kwargs = {'data_id': self.folder.id}
    url = reverse('notes-permissions-create', kwargs=kwargs)
    response = self.client.post(url, share_data)

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with,
      type=choices.PermissionType.READER,
      data=self.folder.id,
    ).exists()

    self.assertFalse(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_editor_user_should_not_update_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=choices.PermissionType.EDITOR
    )

    share_data = {
      'type': self.user_to_share_data_with_permission.type
    }

    kwargs = {
      'data_id': self.folder.id,
      'id': self.user_to_share_data_with_permission.id
    }
    url = reverse('notes-permissions-update', kwargs=kwargs)
    response = self.client.post(url, share_data)

    permission_exists = models.Permission.objects.filter(
      user=self.user,
      type=constants.permissions_relation[self.user_to_share_data_with_permission.type],
      data=self.folder,
    ).exists()

    self.assertFalse(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_editor_user_should_not_delete_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=choices.PermissionType.EDITOR
    )

    kwargs = {
      'data_id': self.folder.id,
      'id': self.user_to_share_data_with_permission.id
    }
    url = reverse('notes-permissions-remove', kwargs=kwargs)
    response = self.client.post(url)

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with_permission.user,
      type=self.user_to_share_data_with_permission.type,
      data=self.user_to_share_data_with_permission.data,
    ).exists()

    self.assertTrue(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_reader_user_should_not_list_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=choices.PermissionType.READER
    )

    kwargs = {'data_id': self.folder.id}
    url = reverse('notes-permissions-list', kwargs=kwargs)
    response = self.client.get(url)

    self.assertEqual(response.status_code, 403)

  def test_reader_user_should_not_create_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=choices.PermissionType.READER
    )

    share_data = {
      'user': self.user_to_share_data_with,
      'type': choices.PermissionType.READER,
      'data': self.folder.id,
    }

    kwargs = {'data_id': self.folder.id}
    url = reverse('notes-permissions-create', kwargs=kwargs)
    response = self.client.post(url, share_data)

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with,
      type=choices.PermissionType.READER,
      data=self.folder.id,
    ).exists()

    self.assertFalse(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_reader_user_should_not_update_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=choices.PermissionType.READER
    )

    share_data = {
      'type': self.user_to_share_data_with_permission.type
    }

    kwargs = {
      'data_id': self.folder.id,
      'id': self.user_to_share_data_with_permission.id
    }
    url = reverse('notes-permissions-update', kwargs=kwargs)
    response = self.client.post(url, share_data)

    permission = models.Permission.objects.get(id=self.user_to_share_data_with_permission.id)

    self.assertTrue(permission.type == self.user_to_share_data_with_permission.type)
    self.assertEqual(response.status_code, 403)

  def test_reader_user_should_not_delete_permissions(self):
    models.Permission.objects.create(
      data=self.folder, user=self.user, type=choices.PermissionType.READER
    )

    kwargs = {
      'data_id': self.folder.id,
      'id': self.user_to_share_data_with_permission.id
    }
    url = reverse('notes-permissions-remove', kwargs=kwargs)
    response = self.client.post(url)

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with_permission.user,
      type=self.user_to_share_data_with_permission.type,
      data=self.user_to_share_data_with_permission.data,
    ).exists()

    self.assertTrue(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_user_without_permission_should_not_list_permissions(self):
    kwargs = {'data_id': self.folder.id}
    url = reverse('notes-permissions-list', kwargs=kwargs)
    response = self.client.get(url)

    self.assertEqual(response.status_code, 403)

  def test_user_without_permission_should_not_create_permissions(self):
    share_data = {
      'user': self.user_to_share_data_with,
      'type': choices.PermissionType.READER,
      'data': self.folder.id,
    }

    kwargs = {'data_id': self.folder.id}
    url = reverse('notes-permissions-create', kwargs=kwargs)
    response = self.client.post(url, share_data)

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with,
      type=choices.PermissionType.READER,
      data=self.folder.id,
    ).exists()

    self.assertFalse(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_user_without_permission_should_not_update_permissions(self):
    share_data = {
      'type': self.user_to_share_data_with_permission.type
    }

    kwargs = {
      'data_id': self.folder.id,
      'id': self.user_to_share_data_with_permission.id
    }
    url = reverse('notes-permissions-update', kwargs=kwargs)
    response = self.client.post(url, share_data)

    permission_exists = models.Permission.objects.filter(
      user=self.user,
      type=constants.permissions_relation[self.user_to_share_data_with_permission.type],
      data=self.folder,
    ).exists()

    self.assertFalse(permission_exists)
    self.assertEqual(response.status_code, 403)

  def test_user_without_permission_should_not_delete_permissions(self):
    kwargs = {
      'data_id': self.folder.id,
      'id': self.user_to_share_data_with_permission.id
    }
    url = reverse('notes-permissions-remove', kwargs=kwargs)
    response = self.client.post(url)

    permission_exists = models.Permission.objects.filter(
      user=self.user_to_share_data_with_permission.user,
      type=self.user_to_share_data_with_permission.type,
      data=self.user_to_share_data_with_permission.data,
    ).exists()

    self.assertTrue(permission_exists)
    self.assertEqual(response.status_code, 403)
