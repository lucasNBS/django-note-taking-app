from django.contrib import auth
from django.test import Client, TestCase

from . import models, utils


# Create your tests here.
class AuthenticationTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = Client()

    def test_register(self):
        register_data = {
            "username": "user",
            "email": "user@email.com",
            "password1": "password",
            "password2": "password",
        }

        self.client.post("/accounts/register/", register_data)
        user_exists = models.User.objects.filter(email=register_data["email"]).exists()

        self.assertTrue(user_exists)

    def test_login(self):
        user = utils.create_default_user()

        login_data = {"username": "user@email.com", "password": "password"}
        self.client.post("/accounts/login/", login_data)
        client_user = auth.get_user(self.client)

        self.assertEqual(user.id, client_user.id)

    def test_logout(self):
        utils.create_default_user()

        login_data = {"username": "user@email.com", "password": "password"}
        self.client.post("/accounts/login/", login_data)
        client_logged_in_user = auth.get_user(self.client)

        self.client.post("/accounts/logout/")
        client_logged_out_user = auth.get_user(self.client)

        self.assertNotEqual(client_logged_in_user.id, client_logged_out_user.id)
