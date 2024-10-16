import datetime
from django.urls import reverse
from django.contrib import auth
from django.test import TestCase, RequestFactory, Client

from accounts import utils
from tags.models import Tag
from permissions.models import Permission
from permissions.choices import PermissionType
from folders.models import Folders

from . import models, views

# Create your tests here.
class NotesOperationsTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client_user = utils.create_default_user()
    self.note = models.Note.objects.create(
      title="Note 1",
      description="Note 1 description",
      content="Note 1 content",
      folder=Folders.objects.get(title="General"),
    )
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.CREATOR)

  def test_list_notes(self):
    request = RequestFactory().get("/")
    request.user = self.client_user

    response = views.ListNoteView.as_view()(request)
    response.render()
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_detail_note(self):
    request = RequestFactory().get("/")
    request.user = self.client_user

    response = views.DetailNoteView.as_view()(request, id=self.note.id)
    response.render()
    self.assertContains(
      response,
      f'<h1 class="text-3xl capitalize font-bold">{self.note.title}</h1>',
      html="True",
    )

  def test_create_note(self):
    note_data = {
      'title': 'Note 2',
      'description': 'Note 2 description',
      'content': 'Note 2 content',
      'folder': Folders.objects.get(title="General").id,
    }

    request = RequestFactory().post("/", note_data)
    request.user = self.client_user

    views.CreateNoteView.as_view()(request)
    note_exists = models.Note.objects.filter(title="Note 2").exists()
    self.assertTrue(note_exists)

  def test_update_note(self):
    note_new_data = {
      'title': 'Note 2 New Title',
      'description': 'Note 2 description',
      'content': 'Note 2 content',
      'folder': Folders.objects.get(title="General").id,
    }

    request = RequestFactory().post("/", note_new_data)
    request.user = self.client_user

    views.UpdateNoteView.as_view()(request, id=self.note.id)
    note_exists = models.Note.objects.filter(title="Note 2 New Title").exists()
    self.assertTrue(note_exists)

  def test_delete_note(self):
    request = RequestFactory().post("/")
    request.user = self.client_user

    views.DeleteNoteView.as_view()(request, id=self.note.id)
    note_exists = models.Note.objects.filter(title="Note 2").exists()
    self.assertFalse(note_exists)

  def test_restore_note(self):
    self.note.delete()

    request = RequestFactory().post("/")
    request.user = self.client_user

    views.restore_note_view(request, id=self.note.id)
    note_exists = models.Note.objects.filter(title="Note 1").exists()
    self.assertTrue(note_exists)

  def test_favorite_note(self):
    request = RequestFactory().post("/")
    request.user = self.client_user

    views.FavoriteNoteView.as_view()(request, id=self.note.id)
    note_is_liked = models.Like.objects.filter(user=self.client_user, note=self.note).exists()
    self.assertTrue(note_is_liked)

class NotesValidationTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client = Client()
    user = utils.create_default_user()
    utils.log_in_default_user(self.client)
    self.client_user = auth.get_user(self.client)
    self.note = models.Note.objects.create(
      title="Note 1",
      description="Note 1 description",
      content="Note 1 content",
      folder=Folders.objects.get(title="General"),
    )

  def setUp(self):
    utils.log_in_default_user(self.client)

  def test_editor_user_should_list_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    self.note.folder = folder
    self.note.save()

    Permission.objects.create(data=folder, user=self.client_user, type=PermissionType.EDITOR)
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.EDITOR)

    kwargs = {'id': folder.id}
    url = reverse('notes-list-folder', kwargs=kwargs)
    response = self.client.get(url)    
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_reader_user_should_list_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    self.note.folder = folder
    self.note.save()

    Permission.objects.create(data=folder, user=self.client_user, type=PermissionType.READER)
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.READER)

    kwargs = {'id': folder.id}
    url = reverse('notes-list-folder', kwargs=kwargs)
    response = self.client.get(url)    
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_user_without_permission_should_not_list_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    self.note.folder = folder
    self.note.save()

    kwargs = {'id': folder.id}
    url = reverse('notes-list-folder', kwargs=kwargs)
    response = self.client.get(url)
    self.assertEquals(response.status_code, 403)

  def test_editor_user_should_detail_note(self):
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.EDITOR)

    kwargs = {'id': self.note.id}
    url = reverse('notes-detail', kwargs=kwargs)
    response = self.client.get(url)    
    self.assertContains(
      response,
      f'<h1 class="text-3xl capitalize font-bold">{self.note.title}</h1>',
      html="True",
    )

  def test_reader_user_should_detail_note(self):
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.READER)

    kwargs = {'id': self.note.id}
    url = reverse('notes-detail', kwargs=kwargs)
    response = self.client.get(url)    
    self.assertContains(
      response,
      f'<h1 class="text-3xl capitalize font-bold">{self.note.title}</h1>',
      html="True",
    )

  def test_user_without_permission_should_not_detail_note(self):
    kwargs = {'id': self.note.id}
    url = reverse('notes-detail', kwargs=kwargs)
    response = self.client.get(url)
    self.assertEquals(response.status_code, 403)

  def test_editor_user_should_create_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    Permission.objects.create(data=folder, user=self.client_user, type=PermissionType.EDITOR)

    note_data = {
      'title': 'Note 2',
      'description': 'Note 2 description',
      'content': 'Note 2 content',
      'folder': folder.id,
    }

    url = reverse('notes-create')
    response = self.client.post(url, note_data)
    note_exists = models.Note.objects.filter(title="Note 2").exists()
    
    self.assertTrue(note_exists)

  def test_reader_user_should_not_create_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    Permission.objects.create(data=folder, user=self.client_user, type=PermissionType.READER)

    note_data = {
      'title': 'Note 2',
      'description': 'Note 2 description',
      'content': 'Note 2 content',
      'folder': folder.id,
    }

    url = reverse('notes-create')
    response = self.client.post(url, note_data)
    note_exists = models.Note.objects.filter(title="Note 2").exists()
    
    self.assertFalse(note_exists)

  def test_user_without_permission_should_not_create_note_in_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    note_data = {
      'title': 'Note 2',
      'description': 'Note 2 description',
      'content': 'Note 2 content',
      'folder': folder.id,
    }

    url = reverse('notes-create')
    response = self.client.post(url, note_data)
    note_exists = models.Note.objects.filter(title="Note 2").exists()

    self.assertFalse(note_exists)

  def test_editor_user_should_update_note(self):
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.EDITOR)

    note_new_data = {
      'title': 'Note 1 New Title',
      'description': 'Note 1 description',
      'content': 'Note 1 content',
      'folder': Folders.objects.get(title="General").id,
    }

    kwargs = {'id': self.note.id}
    url = reverse('notes-update', kwargs=kwargs)
    response = self.client.post(url, note_new_data)
    note_exists = models.Note.objects.filter(title="Note 1 New Title").exists()
    self.assertTrue(note_exists)

  def test_reader_user_should_not_update_note(self):
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.READER)

    note_new_data = {
      'title': 'Note 1 New Title',
      'description': 'Note 1 description',
      'content': 'Note 1 content',
      'folder': Folders.objects.get(title="General").id,
    }

    kwargs = {'id': self.note.id}
    url = reverse('notes-update', kwargs=kwargs)
    response = self.client.post(url, note_new_data)
    note_exists = models.Note.objects.filter(title="Note 1 New Title").exists()
    self.assertFalse(note_exists)

  def test_user_without_permission_should_not_update_note(self):
    note_new_data = {
      'title': 'Note 1 New Title',
      'description': 'Note 1 description',
      'content': 'Note 1 content',
      'folder': Folders.objects.get(title="General").id,
    }

    kwargs = {'id': self.note.id}
    url = reverse('notes-update', kwargs=kwargs)
    response = self.client.post(url, note_new_data)
    note_exists = models.Note.objects.filter(title="Note 1 New Title").exists()
    self.assertFalse(note_exists)

  def test_editor_user_should_not_delete_note(self):
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.EDITOR)

    kwargs = {'id': self.note.id}
    url = reverse('notes-delete', kwargs=kwargs)
    response = self.client.post(url)
    note_still_exists = models.Note.objects.filter(title="Note 1").exists()
    self.assertTrue(note_still_exists)

  def test_reader_user_should_not_delete_note(self):
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.READER)

    kwargs = {'id': self.note.id}
    url = reverse('notes-delete', kwargs=kwargs)
    response = self.client.post(url)
    note_still_exists = models.Note.objects.filter(title="Note 1").exists()
    self.assertTrue(note_still_exists)

  def test_user_without_permission_should_not_delete_note(self):
    kwargs = {'id': self.note.id}
    url = reverse('notes-delete', kwargs=kwargs)
    response = self.client.post(url)
    note_still_exists = models.Note.objects.filter(title="Note 1").exists()
    self.assertTrue(note_still_exists)

  def test_editor_user_should_not_restore_note(self):
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.EDITOR)
    self.note.delete()
    
    kwargs = {'id': self.note.id}
    url = reverse('notes-restore', kwargs=kwargs)
    response = self.client.post(url)
    note_was_restored = models.Note.objects.filter(title="Note 1").exists()
    self.assertFalse(note_was_restored)

  def test_reader_user_should_not_restore_note(self):
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.READER)
    self.note.delete()
    
    kwargs = {'id': self.note.id}
    url = reverse('notes-restore', kwargs=kwargs)
    response = self.client.post(url)
    note_was_restored = models.Note.objects.filter(title="Note 1").exists()
    self.assertFalse(note_was_restored)

  def test_user_without_permission_should_not_restore_note(self):
    self.note.delete()

    kwargs = {'id': self.note.id}
    url = reverse('notes-restore', kwargs=kwargs)
    response = self.client.post(url)
    note_was_restored = models.Note.objects.filter(title="Note 1").exists()
    self.assertFalse(note_was_restored)

class NotesListTypesTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client_user = utils.create_default_user()
    self.note = models.Note.objects.create(
      title="Note 1",
      description="Note 1 description",
      content="Note 1 content",
      folder=Folders.objects.filter(title="General").first(),
    )
    self.note_permission = Permission.objects.create(
      data=self.note, user=self.client_user, type=PermissionType.CREATOR
    )

  def test_list_deleted_notes(self):
    self.note.delete()

    request = RequestFactory().get("/")
    request.user = self.client_user

    response = views.ListDeletedNoteView.as_view()(request)
    response.render()
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_list_favorite_notes(self):
    models.Like.objects.create(user=self.client_user, note=self.note)

    request = RequestFactory().get("/")
    request.user = self.client_user

    response = views.ListFavoriteNoteView.as_view()(request)
    response.render()
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_list_shared_notes(self):
    note_permission = Permission.objects.filter(id=self.note_permission.id)
    note_permission.update(type=PermissionType.READER)

    request = RequestFactory().get("/")
    request.user = self.client_user

    response = views.ListSharedNoteView.as_view()(request)
    response.render()
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_list_notes_by_tag(self):
    tag = Tag.objects.create(title="Tag 1", created_by=self.client_user)
    self.note.tags.add(tag)

    request = RequestFactory().get("/")
    request.user = self.client_user

    response = views.ListTagNotesView.as_view()(request, id=tag.id)
    response.render()
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_list_notes_by_folder(self):
    folder = Folders.objects.create(title="Folder 1")
    Permission.objects.create(data=folder, user=self.client_user, type=PermissionType.CREATOR)
    self.note.folder = folder
    self.note.save()

    request = RequestFactory().get("/")
    request.user = self.client_user

    response = views.ListFolderNotesView.as_view()(request, id=folder.id)
    response.render()
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

class NotesFilterTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client_user = utils.create_default_user()
    self.note = models.Note.objects.create(
      title="Note 1",
      description="Note 1 description",
      content="Note 1 content",
      folder=Folders.objects.get(title="General"),
    )
    self.note.created_at = datetime.datetime(2024, 1, 1, 12, 0, 0, 0)
    self.note.save()
    Permission.objects.create(data=self.note, user=self.client_user, type=PermissionType.CREATOR)

  def test_filter_notes_by_title(self):
    filter_data = {
      'title': 'Note',
    }

    request = RequestFactory().get("/", filter_data)
    request.user = self.client_user

    response = views.ListNoteView.as_view()(request)
    response.render()
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_filter_notes_by_non_existent_title(self):
    filter_data = {
      'title': 'Nota',
    }

    request = RequestFactory().get("/", filter_data)
    request.user = self.client_user

    response = views.ListNoteView.as_view()(request)
    response.render()
    self.assertNotContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_filter_notes_by_date(self):
    filter_data = {
      'start-date': datetime.datetime(2024, 1, 1),
      'end-date': datetime.datetime(2024, 1, 2),
    }

    request = RequestFactory().get("/", filter_data)
    request.user = self.client_user

    response = views.ListNoteView.as_view()(request)
    response.render()
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_filter_notes_by_non_correspondent_date(self):
    filter_data = {
      'start-date': datetime.datetime(2024, 1, 2),
      'end-date': datetime.datetime(2024, 1, 3),
    }

    request = RequestFactory().get("/", filter_data)
    request.user = self.client_user

    response = views.ListNoteView.as_view()(request)
    response.render()
    self.assertNotContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_filter_notes_by_tags(self):
    tag = Tag.objects.create(title="Tag 1", created_by=self.client_user)
    self.note.tags.add(tag)

    filter_data = {
      'tags': tag.id,
    }

    request = RequestFactory().get("/", filter_data)
    request.user = self.client_user

    response = views.ListNoteView.as_view()(request)
    response.render()
    self.assertContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )

  def test_filter_notes_by_non_correspondent_tags(self):
    tag = Tag.objects.create(title="Tag 1", created_by=self.client_user)

    filter_data = {
      'tags': tag.id,
    }

    request = RequestFactory().get("/", filter_data)
    request.user = self.client_user

    response = views.ListNoteView.as_view()(request)
    response.render()
    self.assertNotContains(
      response,
      f'<h2 class="font-bold text-xl max-h-20 capitalize cursor-pointer overflow-hidden w-fit transition-transform hover:scale-110">{self.note.title}</h2>',
      html="True",
    )
