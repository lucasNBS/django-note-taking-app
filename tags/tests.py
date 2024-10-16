from django.contrib import auth
from django.test import TestCase, RequestFactory

from accounts import utils

from . import models, views

# Create your tests here.
class TagsOperationsTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client_user = utils.create_default_user()
    self.tag = models.Tag.objects.create(title="Tag 1", created_by=self.client_user)

  def test_create_tag(self):
    tag_data = {
      'title': 'Tag 2'
    }

    request = RequestFactory().post("/", tag_data)
    request.user = self.client_user

    views.CreateTagView.as_view()(request)
    tag_exists = models.Tag.objects.filter(title="Tag 2").exists()
    self.assertTrue(tag_exists)

  def test_update_tag(self):
    tag_new_data = {
      'title': 'Tag 1 New Title'
    }
    request = RequestFactory().post("/", tag_new_data)
    request.user = self.client_user

    views.UpdateTagView.as_view()(request, id=self.tag.id)
    tag_exists = models.Tag.objects.filter(title="Tag 1 New Title").exists()
    self.assertTrue(tag_exists)

  def test_delete_tag(self):
    request = RequestFactory().post("/")
    request.user = self.client_user

    views.DeleteTagView.as_view()(request, id=self.tag.id)
    tag_exists = models.Tag.objects.filter(title="Tag 1").exists()
    self.assertFalse(tag_exists)

class TagsAutocompleteTestCase(TestCase):
  @classmethod
  def setUpTestData(self):
    self.client_user = utils.create_default_user()
    self.tag = models.Tag.objects.create(title="Tag 1", created_by=self.client_user)

  def test_autocomplete_list_tag(self):
    search_data = {'search': 'Tag 1'}

    request = RequestFactory().get("/", search_data)
    request.user = self.client_user

    response = views.autocomplete_tag_view(request)

    self.assertJSONEqual(response.content, [{"title": "Tag 1", "id": self.tag.id}])

  def test_autocomplete_not_list_non_user_tags(self):
    user_that_doesnt_have_access_to_existent_tag = utils.create_user(
      username='teste',
      email='teste@email.com',
      password='teste',
    )

    search_data = {'search': 'Tag 1'}

    request = RequestFactory().get("/", search_data)
    request.user = user_that_doesnt_have_access_to_existent_tag

    response = views.autocomplete_tag_view(request)

    self.assertJSONEqual(response.content, [])
