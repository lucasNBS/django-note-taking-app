from rest_framework import exceptions
from ..models import User
import jwt

def get_user(request):
  access_token = request.COOKIES.get('access_token')

  try:
    payload = jwt.decode(access_token, 'SECRET', algorithms=['HS256'])

    user = User.objects.filter(id=payload['id']).first()

    return user
  except:
    raise exceptions.AuthenticationFailed('Unauthenticated')