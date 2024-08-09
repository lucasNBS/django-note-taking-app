from django.urls import path
from .views import RegisterView, CustomLoginView, logout_view

urlpatterns = [
  path("login/", CustomLoginView.as_view(), name='accounts-login'),
  path("logout/", logout_view, name='accounts-logout'),
  path("register/", RegisterView.as_view(), name='accounts-register'),
]
