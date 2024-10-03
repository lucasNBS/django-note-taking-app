from django.urls import path, include
from rest_framework import routers
from .views import NotesView

router = routers.DefaultRouter()
router.register('', NotesView)

urlpatterns = [
  path('', include(router.urls))
]
