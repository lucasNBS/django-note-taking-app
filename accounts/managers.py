from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
  def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
    if not username:
        raise ValueError("Username is required")
    email = self.normalize_email(email)
    user = self.model(username=username, email=email, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, username, email=None, password=None, **extra_fields):
    return self._create_user(username, email, password, False, False, **extra_fields)

  def create_superuser(self, username, email, password, **extra_fields):
    user=self._create_user(username, email, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user