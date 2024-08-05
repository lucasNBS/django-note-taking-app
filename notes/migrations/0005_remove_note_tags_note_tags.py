# Generated by Django 5.0.7 on 2024-08-04 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_note_tags'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='tags',
        ),
        migrations.AddField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='tags.tag'),
        ),
    ]
