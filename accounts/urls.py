from django.urls import include, path

from .views import LoginView, RegisterView, logout_view

urlpatterns = [
    path("login/", LoginView.as_view(), name="accounts-login"),
    path("logout/", logout_view, name="accounts-logout"),
    path("register/", RegisterView.as_view(), name="accounts-register"),
    path("api/", include("accounts.api.urls")),
]
