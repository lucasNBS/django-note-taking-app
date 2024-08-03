from django.shortcuts import redirect

def redirect_home(self):
  return redirect('notes-list')