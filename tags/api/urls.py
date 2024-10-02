from django.urls import path, include
from rest_framework import routers
from .views import TagView

router = routers.DefaultRouter()
router.register('', TagView)

urlpatterns = [
  path('', include(router.urls))
]