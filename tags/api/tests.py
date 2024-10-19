from rest_framework.test import APIRequestFactory, APITestCase

from accounts import utils

from .. import models
from . import views


# Create your tests here.
class TagAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.user = utils.create_default_user()
        self.tag = models.Tag.objects.create(title="Tag 1", created_by=self.user)

    def setUp(self):
        utils.log_in_default_user(self.client)

    def test_api_create_tag(self):
        tag_data = {"title": "Tag 2"}

        request = APIRequestFactory().post("/", tag_data)
        request.user = self.user

        views.TagView.as_view({"post": "create"})(request)
        tag_exists = models.Tag.objects.filter(title="Tag 2").exists()
        self.assertTrue(tag_exists)

    def test_api_update_tag(self):
        tag_new_data = {"title": "Tag 1 New Title"}

        request = APIRequestFactory().post("/", tag_new_data)
        request.user = self.user

        views.TagView.as_view({"post": "update"})(request, pk=self.tag.id)
        tag_exists = models.Tag.objects.filter(title="Tag 1 New Title").exists()
        self.assertTrue(tag_exists)

    def test_api_delete_tag(self):
        request = APIRequestFactory().post("/")
        request.user = self.user

        views.TagView.as_view({"post": "destroy"})(request, pk=self.tag.id)
        tag_still_exists = models.Tag.objects.filter(title="Tag 1").exists()
        self.assertFalse(tag_still_exists)
