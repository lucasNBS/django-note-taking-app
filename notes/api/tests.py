import datetime
from rest_framework.test import APITestCase, APIRequestFactory

from accounts import utils
from accounts.api.utils import get_user
from permissions.models import Permission
from permissions.choices import PermissionType
from folders.models import Folders
from tags.models import Tag

from . import views
from .. import models

# Create your tests here.
class NoteOperationsAPITestCase(APITestCase):
  @classmethod
  def setUpTestData(self):
    self.user = utils.create_default_user()
    self.note = models.Note.objects.create(
      title="Note 1",
      description="Note 1 description",
      content="Note 1 content",
      folder=Folders.objects.get(title="General"),
    )
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.CREATOR)

  def test_api_list_notes(self):
    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'list'})(request)
    response.render()

    self.assertIn("Note 1", str(response.content))

  def test_api_detail_note(self):
    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'retrieve'})(request, pk=self.note.id)
    response.render()

    self.assertIn("Note 1", str(response.content))

  def test_api_create_note(self):
    note_data = {
      'title': 'Note 2',
      'description': 'Note 2 description',
      'content': 'Note 2 content',
      'folder': Folders.objects.get(title="General").id,
    }

    request = APIRequestFactory().post("/", note_data)
    request.user = self.user

    response = views.NotesView.as_view({'post': 'create'})(request)

    note_exists = models.Note.objects.filter(title="Note 2").exists()
    self.assertTrue(note_exists)
    self.assertEqual(response.status_code, 201)

  def test_api_update_note(self):
    note_new_data = {
      'title': 'Note 1 New Title',
      'description': 'Note 1 New description',
      'content': 'Note 1 New content',
      'folder': Folders.objects.get(title="General").id,
    }

    request = APIRequestFactory().post("/", note_new_data)
    request.user = self.user

    response = views.NotesView.as_view({'post': 'update'})(request, pk=self.note.id)
    response.render()

    note_exists = models.Note.objects.filter(title="Note 1 New Title").exists()
    self.assertTrue(note_exists)
    self.assertEqual(response.status_code, 200)

  def test_api_delete_note(self):
    request = APIRequestFactory().post("/")
    request.user = self.user

    response = views.NotesView.as_view({'post': 'destroy'})(request, pk=self.note.id)

    note_still_exists = models.Note.objects.filter(title="Note 1").exists()
    self.assertFalse(note_still_exists)
    self.assertEqual(response.status_code, 204)

  def test_api_restore_note(self):
    self.note.delete()

    request = APIRequestFactory().post("/")
    request.user = self.user

    views.NotesView.as_view({'post': 'restore_note'})(request, pk=self.note.id)

    note_exists = models.Note.objects.filter(title="Note 1").exists()
    self.assertTrue(note_exists)

  def test_api_favorite_note(self):
    request = APIRequestFactory().post("/")
    request.user = self.user

    views.NotesView.as_view({'post': 'favorite'})(request, pk=self.note.id)

    note_is_liked = models.Like.objects.filter(user=self.user, note=self.note).exists()
    self.assertTrue(note_is_liked)

class NotesValidationAPITestCase(APITestCase):
  @classmethod
  def setUpTestData(self):
    self.user = utils.create_default_user()
    self.note = models.Note.objects.create(
      title="Note 1",
      description="Note 1 description",
      content="Note 1 content",
      folder=Folders.objects.get(title="General"),
    )

  def test_api_editor_user_should_list_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    self.note.folder = folder
    self.note.save()

    Permission.objects.create(data=folder, user=self.user, type=PermissionType.EDITOR)
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.EDITOR)

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'folder'})(request, pk=folder.id)
    response.render()
    self.assertIn("Note 1", str(response.content))

  def test_api_reader_user_should_list_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    self.note.folder = folder
    self.note.save()

    Permission.objects.create(data=folder, user=self.user, type=PermissionType.READER)
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.READER)

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'folder'})(request, pk=folder.id)
    response.render()
    self.assertIn("Note 1", str(response.content))

  def test_api_user_without_permission_should_not_list_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    self.note.folder = folder
    self.note.save()

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'folder'})(request, pk=folder.id)

    self.assertEquals(response.status_code, 403)

  def test_api_editor_user_should_detail_note(self):
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.EDITOR)

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'retrieve'})(request, pk=self.note.id)
    response.render()
    self.assertIn("Note 1", str(response.content))

  def test_api_reader_user_should_detail_note(self):
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.READER)

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'retrieve'})(request, pk=self.note.id)
    response.render()
    self.assertIn("Note 1", str(response.content))

  def test_api_user_without_permission_should_not_detail_note(self):
    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'retrieve'})(request, pk=self.note.id)
    self.assertEquals(response.status_code, 403)

  def test_api_editor_user_should_create_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    Permission.objects.create(data=folder, user=self.user, type=PermissionType.EDITOR)

    note_data = {
      'title': 'Note 2',
      'description': 'Note 2 description',
      'content': 'Note 2 content',
      'folder': folder.id,
    }

    request = APIRequestFactory().post("/", note_data)
    request.user = self.user

    response = views.NotesView.as_view({'post': 'create'})(request)
    note_exists = models.Note.objects.filter(title="Note 2").exists()
    self.assertTrue(note_exists)

  def test_api_reader_user_should_not_create_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    Permission.objects.create(data=folder, user=self.user, type=PermissionType.READER)

    note_data = {
      'title': 'Note 2',
      'description': 'Note 2 description',
      'content': 'Note 2 content',
      'folder': folder.id,
    }

    request = APIRequestFactory().post("/", note_data)
    request.user = self.user

    response = views.NotesView.as_view({'post': 'create'})(request)
    note_exists = models.Note.objects.filter(title="Note 2").exists()
    self.assertFalse(note_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_user_without_permission_should_not_create_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    note_data = {
      'title': 'Note 2',
      'description': 'Note 2 description',
      'content': 'Note 2 content',
      'folder': folder.id,
    }

    request = APIRequestFactory().post("/", note_data)
    request.user = self.user

    response = views.NotesView.as_view({'post': 'create'})(request)
    note_exists = models.Note.objects.filter(title="Note 2").exists()

    self.assertFalse(note_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_editor_user_should_update_note(self):
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.EDITOR)

    note_new_data = {
      'title': 'Note 1 New Title',
      'description': 'Note 1 description',
      'content': 'Note 1 content',
      'folder': Folders.objects.get(title="General").id,
    }

    request = APIRequestFactory().post("/", note_new_data)
    request.user = self.user

    response = views.NotesView.as_view({'post': 'update'})(request, pk=self.note.id)
    note_exists = models.Note.objects.filter(title="Note 1 New Title").exists()
    self.assertTrue(note_exists)

  def test_api_reader_user_should_not_update_note(self):
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.READER)

    note_new_data = {
      'title': 'Note 1 New Title',
      'description': 'Note 1 description',
      'content': 'Note 1 content',
      'folder': Folders.objects.get(title="General").id,
    }

    request = APIRequestFactory().post("/", note_new_data)
    request.user = self.user

    response = views.NotesView.as_view({'post': 'update'})(request, pk=self.note.id)
    note_exists = models.Note.objects.filter(title="Note 1 New Title").exists()

    self.assertFalse(note_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_user_without_permission_should_not_update_note(self):
    note_new_data = {
      'title': 'Note 1 New Title',
      'description': 'Note 1 description',
      'content': 'Note 1 content',
      'folder': Folders.objects.get(title="General").id,
    }

    request = APIRequestFactory().post("/", note_new_data)
    request.user = self.user

    response = views.NotesView.as_view({'post': 'update'})(request, pk=self.note.id)
    note_exists = models.Note.objects.filter(title="Note 1 New Title").exists()
    self.assertFalse(note_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_editor_user_should_not_delete_note(self):
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.EDITOR)

    request = APIRequestFactory().post("/")
    request.user = self.user

    response = views.NotesView.as_view({'post': 'destroy'})(request, pk=self.note.id)
    note_still_exists = models.Note.objects.filter(title="Note 1").exists()
    self.assertTrue(note_still_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_reader_user_should_not_delete_note(self):
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.READER)

    request = APIRequestFactory().post("/")
    request.user = self.user

    response = views.NotesView.as_view({'post': 'destroy'})(request, pk=self.note.id)
    note_still_exists = models.Note.objects.filter(title="Note 1").exists()
    self.assertTrue(note_still_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_user_without_permission_should_not_delete_note(self):
    request = APIRequestFactory().post("/")
    request.user = self.user

    response = views.NotesView.as_view({'post': 'destroy'})(request, pk=self.note.id)
    note_still_exists = models.Note.objects.filter(title="Note 1").exists()
    self.assertTrue(note_still_exists)
    self.assertEqual(response.status_code, 403)

  def test_api_editor_user_should_not_restore_note(self):
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.EDITOR)
    self.note.delete()
    
    request = APIRequestFactory().post("/")
    request.user = self.user

    response = views.NotesView.as_view({'post': 'restore_note'})(request, pk=self.note.id)
    note_was_restored = models.Note.objects.filter(title="Note 1").exists()
    self.assertFalse(note_was_restored)
    self.assertEqual(response.status_code, 403)

  def test_api_reader_user_should_not_restore_note(self):
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.READER)
    self.note.delete()
    
    request = APIRequestFactory().post("/")
    request.user = self.user

    response = views.NotesView.as_view({'post': 'restore_note'})(request, pk=self.note.id)
    note_was_restored = models.Note.objects.filter(title="Note 1").exists()
    self.assertFalse(note_was_restored)
    self.assertEqual(response.status_code, 403)

  def test_api_user_without_permission_should_not_restore_note(self):
    self.note.delete()

    request = APIRequestFactory().post("/")
    request.user = self.user

    response = views.NotesView.as_view({'post': 'restore_note'})(request, pk=self.note.id)
    note_was_restored = models.Note.objects.filter(title="Note 1").exists()
    self.assertFalse(note_was_restored)
    self.assertEqual(response.status_code, 403)

class NotesListTypesAPITestCase(APITestCase):
  @classmethod
  def setUpTestData(self):
    self.user = utils.create_default_user()
    self.note = models.Note.objects.create(
      title="Note 1",
      description="Note 1 description",
      content="Note 1 content",
      folder=Folders.objects.filter(title="General").first(),
    )
    self.note_permission = Permission.objects.create(
      data=self.note, user=self.user, type=PermissionType.CREATOR
    )

  def test_api_list_deleted_notes(self):
    self.note.delete()

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'trash'})(request, pk=self.note.id)
    response.render()
    self.assertIn("Note 1", str(response.content))

  def test_api_list_favorite_notes(self):
    models.Like.objects.create(user=self.user, note=self.note)

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'starred'})(request, pk=self.note.id)
    response.render()
    self.assertIn("Note 1", str(response.content))

  def test_api_list_shared_notes(self):
    note_permission = Permission.objects.filter(id=self.note_permission.id)
    note_permission.update(type=PermissionType.READER)

    request = APIRequestFactory().get("/")
    request.user = self.user

    response = views.NotesView.as_view({'get': 'shared'})(request, pk=self.note.id)
    response.render()
    self.assertIn("Note 1", str(response.content))

class NotesFilterAPITestCase(APITestCase):
  @classmethod
  def setUpTestData(self):
    self.user = utils.create_default_user()
    self.note = models.Note.objects.create(
      title="Note 1",
      description="Note 1 description",
      content="Note 1 content",
      folder=Folders.objects.get(title="General"),
    )
    self.note.created_at = datetime.datetime(2024, 1, 1, 12, 0, 0, 0)
    self.note.save()
    Permission.objects.create(data=self.note, user=self.user, type=PermissionType.CREATOR)

  def test_api_filter_notes_by_title(self):
    filter_data = {
      'title': 'Note',
    }

    request = APIRequestFactory().get("/", filter_data)
    request.user = self.user

    response = views.NotesView.as_view({'get': 'list'})(request)
    response.render()
    self.assertIn("Note 1", str(response.content))

  def test_api_filter_notes_by_non_existent_title(self):
    filter_data = {
      'title': 'Nota',
    }

    request = APIRequestFactory().get("/", filter_data)
    request.user = self.user

    response = views.NotesView.as_view({'get': 'list'})(request)
    response.render()
    self.assertIn('"count":0', str(response.content))

  def test_api_filter_notes_by_date(self):
    filter_data = {
      'start-date': datetime.datetime(2024, 1, 1),
      'end-date': datetime.datetime(2024, 1, 2),
    }

    request = APIRequestFactory().get("/", filter_data)
    request.user = self.user

    response = views.NotesView.as_view({'get': 'list'})(request)
    response.render()
    self.assertIn("Note 1", str(response.content))

  def test_api_filter_notes_by_non_correspondent_date(self):
    filter_data = {
      'start-date': datetime.datetime(2024, 1, 2),
      'end-date': datetime.datetime(2024, 1, 3),
    }

    request = APIRequestFactory().get("/", filter_data)
    request.user = self.user

    response = views.NotesView.as_view({'get': 'list'})(request)
    response.render()
    self.assertIn('"count":0', str(response.content))

  def test_api_filter_notes_by_tags(self):
    tag = Tag.objects.create(title="Tag 1", created_by=self.user)
    self.note.tags.add(tag)

    filter_data = {
      'tags': tag.id,
    }

    request = APIRequestFactory().get("/", filter_data)
    request.user = self.user

    response = views.NotesView.as_view({'get': 'list'})(request)
    response.render()
    self.assertIn("Note 1", str(response.content))

  def test_api_filter_notes_by_non_correspondent_tags(self):
    tag = Tag.objects.create(title="Tag 1", created_by=self.user)

    filter_data = {
      'tags': tag.id,
    }

    request = APIRequestFactory().get("/", filter_data)
    request.user = self.user

    response = views.NotesView.as_view({'get': 'list'})(request)
    response.render()
    self.assertIn('"count":0', str(response.content))
