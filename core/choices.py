from django.db import models


class DataType(models.TextChoices):
    NOTE = "NOTE", "Nota"
    FOLDER = "FOLDER", "Pasta"
