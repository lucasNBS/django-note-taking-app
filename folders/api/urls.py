from django.urls import include, path
from rest_framework import routers

from .views import FoldersView

router = routers.DefaultRouter()
router.register("", FoldersView)

urlpatterns = [path("", include(router.urls))]
