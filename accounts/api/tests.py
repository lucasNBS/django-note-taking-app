from django.urls import reverse
from django.contrib import auth
from rest_framework.test import APITestCase
from django.test import RequestFactory
from .. import models, utils

# Create your tests here.
class AuthenticationAPITestCase(APITestCase):

  def test_api_register(self):
    register_data = {
      'username': 'user',
      'email': 'user@email.com',
      'password': 'password',
    }

    url = reverse('accounts-api-register')
    self.client.post(url, register_data)

    user_exists = models.User.objects.filter(email=register_data["email"]).exists()
    self.assertTrue(user_exists)

  def test_api_login(self):
    user = utils.create_default_user()

    login_data = {'email': 'user@email.com', 'password': 'password'}
    login_url = reverse('accounts-api-login')
    self.client.post(login_url, login_data)

    user_data_url = reverse('accounts-api-user')
    response = self.client.get(user_data_url)

    logged_in_user_email = response.data["email"]
    self.assertEqual(login_data["email"], logged_in_user_email)

  def test_api_logout(self):
    user = utils.create_default_user()

    login_data = {'email': 'user@email.com', 'password': 'password'}
    login_url = reverse('accounts-api-login')
    self.client.post(login_url, login_data)

    logout_url = reverse('accounts-api-logout')
    self.client.post(logout_url)

    user_data_url = reverse('accounts-api-user')
    response = self.client.get(user_data_url)
    
    self.assertEqual(response.status_code, 403)
    with self.assertRaises(KeyError):
      response.data["email"]
