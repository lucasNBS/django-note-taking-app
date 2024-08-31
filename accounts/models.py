from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(max_length=50)
  email = models.EmailField(unique=True)
  is_superuser = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ('username',)

  objects = UserManager()