from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from core import widgets

class RegisterForm(UserCreationForm):
  username = forms.CharField(widget=widgets.InputField(label="Username", small=True))
  email = forms.CharField(widget=widgets.InputField(label="E-mail", small=True, type="email"))
  password1 = forms.CharField(
    widget=widgets.InputField(label="Password", small=True, type="password")
  )
  password2 = forms.CharField(
    widget=widgets.InputField(label="Confirm Password", small=True, type="password")
  )
  
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=widgets.InputField(label="E-mail", small=True, type="email"))
  password = forms.CharField(
    widget=widgets.InputField(label="Password", small=True, type="password")
  )
  
  class Meta:
    model = User
    fields = ['username', 'password']