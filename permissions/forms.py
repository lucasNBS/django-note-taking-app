from django import forms

from core import widgets
from accounts.models import User

from .models import Permission
from .choices import AllowToCreatePermissionType

from . import choices, constants

class PermissionCreateForm(forms.ModelForm):
  user = forms.EmailField(
    widget=widgets.InputField(type="email", small=True, placeholder="user@email.com", style_class="h-[40px] w-full")
  )
  
  class Meta:
    model = Permission
    fields = '__all__'
    widgets = {
      "type": forms.Select(attrs={"class": "bg-white h-[40px] rounded"})
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['type'].choices = AllowToCreatePermissionType
  
  def clean_user(self):
    email = self.cleaned_data["user"]
    user = User.objects.get(email=email)
    return user


class PermissionUpdateForm(forms.ModelForm):

  class Meta:
    model = Permission
    fields = ['type',]

  def save(self, commit=True):
    self.instance.type = constants.permissions_relation[self.instance.type]
    self.instance.save()
    return super().save(commit)