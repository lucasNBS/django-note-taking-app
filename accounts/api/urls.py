from django.urls import path, include
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, UserAPIView

urlpatterns = [
  path("login/", LoginAPIView.as_view(), name='accounts-api-login'),
  path("logout/", LogoutAPIView.as_view(), name='accounts-api-logout'),
  path("register/", RegisterAPIView.as_view(), name='accounts-api-register'),
  path("user/", UserAPIView.as_view(), name='accounts-api-user'),
]
