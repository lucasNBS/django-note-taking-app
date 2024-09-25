from .models import User

def create_default_user():
  user = User.objects.create(
      username='user',
      email='user@email.com'
    )
  user.set_password('password')
  user.save()

  return user

def log_in_default_user(client):
  client.login(username='user@email.com', password='password')