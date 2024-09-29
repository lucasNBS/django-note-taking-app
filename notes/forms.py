from django.db.models import Q
from django import forms
from django.core.exceptions import ValidationError
from notes.models import Note, Like
from folders.models import Folders
from permissions.models import Permission
from permissions.choices import PermissionType
from core import widgets, choices

class NoteForm(forms.ModelForm):
  title = forms.CharField(widget=widgets.InputField(label="Title"))
  description = forms.CharField(widget=widgets.InputField(label="Description"))
  content = forms.CharField(widget=widgets.Textarea(label="Content"))

  class Meta:
    model = Note
    fields = ['title', 'description', 'tags', 'folder', 'content']
    widgets = {
      'tags': widgets.SelectMultiple(label="Tags"),
      'folder': widgets.Select(label="Folder")
    }

  def __init__(self, creator=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.creator = creator

  def clean_folder(self):
    folder = self.cleaned_data['folder']

    # Allow user to create notes in 'General' Folder
    if folder.id == Folders.objects.filter(title="General").first().id:
      return folder
    
    permission = Permission.objects.filter(
      data__id=folder.id, user=self.creator
    ).exclude(type=PermissionType.READER).exists()

    if not permission:
      raise ValidationError("You do not have access to edit the selected folder")
    
    return folder

  def clean_tags(self):
    tags = self.cleaned_data['tags']
    tags_user_has_not_access = tags.exclude(created_by=self.creator)

    if len(tags_user_has_not_access) > 0:
      raise ValidationError("You do not have access to some of the selected Tags")

    return tags

  def clean_title(self):
    title = self.cleaned_data["title"]
    if len(title) > 50:
      raise ValidationError("Max length is 50")
    return title

  def clean_description(self):
    description = self.cleaned_data["description"]
    if len(description) > 200:
      raise ValidationError("Max length is 200")
    return description

  def _handle_alter_permission_from_previous_folder(
    self, previous_note_instance, previous_folder_permissions
  ):
    for folder_permission in previous_folder_permissions:
      note_previous_permission = Permission.objects.filter(
        data=previous_note_instance, type=folder_permission.type, user=folder_permission.user
      ).first()
      if note_previous_permission:
        note_previous_permission.delete()

  def _handle_alter_permission_from_new_folder(
    self, new_note_instance, new_folder_permissions
  ):
    for folder_permission in new_folder_permissions:
      permission = Permission.objects.filter(
        data=new_note_instance, type=folder_permission.type, user=folder_permission.user
      ).first()
      if not permission:
        Permission.objects.create(
          data=new_note_instance, type=folder_permission.type, user=folder_permission.user
        )

  def _handle_alter_permission_when_folder_change(self, previous_note_instance, new_note_instance):
    previous_folder_permissions = Permission.objects.filter(
      data=previous_note_instance.folder
    ).exclude(type=PermissionType.CREATOR)

    if previous_folder_permissions and previous_note_instance.folder.title != "General":
      self._handle_alter_permission_from_previous_folder(
        previous_note_instance, previous_folder_permissions
      )

    new_folder_permissions = Permission.objects.filter(
      data=new_note_instance.folder
    ).exclude(type=PermissionType.CREATOR)
    
    if new_folder_permissions and new_note_instance.folder.title != "General":
      self._handle_alter_permission_from_new_folder(
        new_note_instance, new_folder_permissions
      )

  def save(self, *args, **kwargs):
    created = True if self.instance.id else False

    if created:
      previous_note_instance = Note.objects.get(id=self.instance.id)
      if self.instance.folder != previous_note_instance.folder:
        self._handle_alter_permission_when_folder_change(previous_note_instance, self.instance)

    save = super().save(*args, **kwargs)

    if self.creator is not None and not created:
      Permission.objects.create(
        user=self.creator, type=PermissionType.CREATOR, data=self.instance
      )

    return save

class UpdateSharedNoteForm(forms.ModelForm):
  title = forms.CharField(widget=widgets.InputField(label="Title"))
  description = forms.CharField(widget=widgets.InputField(label="Description"))
  content = forms.CharField(widget=widgets.Textarea(label="Content"))

  class Meta:
    model = Note
    fields = ['title', 'description', 'tags', 'content']
    widgets = {
      'tags': widgets.SelectMultiple(label="Tags"),
    }

  def __init__(self, creator=None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.creator = creator

  def clean_tags(self):
    tags = self.cleaned_data['tags']
    tags_user_has_not_access = tags.exclude(created_by=self.creator)

    if len(tags_user_has_not_access) > 0:
      raise ValidationError("You do not have access to some of the selected Tags")

    return tags

  def clean_title(self):
    title = self.cleaned_data["title"]
    if len(title) > 50:
      raise ValidationError("Max length is 50")
    return title

  def clean_description(self):
    description = self.cleaned_data["description"]
    if len(description) > 200:
      raise ValidationError("Max length is 200")
    return description
  
  def save(self, *args, **kwargs):
    if self.creator is not None:
      self.instance.created_by = self.creator
    return super().save(*args, **kwargs)


class FavoriteNoteForm(forms.ModelForm):
  
  class Meta:
    model = Like
    fields = ['user', 'note']

  def save(self, *args, **kwargs):
    like = Like.objects.filter(user=self.data['user'], note__id=self.data['note'])

    if len(like) > 0:
      like.delete()
      return self

    return super().save(*args, **kwargs)