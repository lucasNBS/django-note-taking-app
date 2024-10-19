from django.urls import include, path
from rest_framework import routers

from .views import TagView

router = routers.DefaultRouter()
router.register("", TagView, basename="tags-api")

urlpatterns = [path("", include(router.urls))]
