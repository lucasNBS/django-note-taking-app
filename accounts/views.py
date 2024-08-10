from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import views
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from .forms import RegisterForm, LoginForm

# Create your views here.
class RegisterView(CreateView):
  form_class = RegisterForm
  template_name = 'accounts/form.html'
  success_url = reverse_lazy('accounts-login')
  title = "Register"
  text = "Sign Up"
  subtext = "Already have an account?"
  link_text = "Login"
  url = "/accounts/login/"

  def form_valid(self, form):
    user = form.save()

    if user:
      login(self.request, user)

    return super().form_valid(form)
  
class LoginView(views.LoginView):
  form_class = LoginForm
  template_name = 'accounts/form.html'
  success_url = reverse_lazy('notes-list')
  redirect_authenticated_user = True
  title = "Login"
  text = "Sign In"
  subtext = "Don't have an account yet?"
  link_text = "Register"
  url = "/accounts/register/"

def logout_view(request):
  logout(request)
  return redirect('notes-list')