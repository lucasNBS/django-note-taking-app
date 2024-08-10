# Generated by Django 5.0.7 on 2024-08-10 14:33

import django.db.models.deletion
import folders.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0001_initial'),
        ('notes', '0003_note_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='folder',
            field=models.ForeignKey(default=folders.models.Folders.get_default_id, on_delete=django.db.models.deletion.PROTECT, to='folders.folders'),
        ),
    ]
