from .models import User

def create_user(username, email, password):
  user = User.objects.create(username=username, email=email)
  user.set_password(password)
  user.save()

  return user

def log_in_user(client, username, password):
  client.login(username=username, password=password)

def create_default_user():
  return create_user(
    username='user',
    email='user@email.com',
    password='password'
  )

def log_in_default_user(client):
  log_in_user(client, username='user@email.com', password='password')
