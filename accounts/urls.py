from django.urls import path
from .views import RegisterView, LoginView, logout_view

urlpatterns = [
  path("login/", LoginView.as_view(), name='accounts-login'),
  path("logout/", logout_view, name='accounts-logout'),
  path("register/", RegisterView.as_view(), name='accounts-register'),
]
