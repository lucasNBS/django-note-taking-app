from django.urls import path, include
from rest_framework import routers
from .views import FoldersView

router = routers.DefaultRouter()
router.register('', FoldersView)

urlpatterns = [
  path('', include(router.urls))
]