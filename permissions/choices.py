from django.db import models

class PermissionType(models.TextChoices):
  READER = "READER", "Leitor"
  EDITOR = "EDITOR", "Editor"
  CREATOR = "CREATOR", "Criador"
