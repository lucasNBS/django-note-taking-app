from rest_framework.response import Response
from rest_framework import views, exceptions
import jwt, datetime

from .serializers import UserSerializer
from ..models import User

def create_payload(user):
  return {
    'id': user.id,
    'exp': datetime.datetime.now() + datetime.timedelta(minutes=15),
    'iat': datetime.datetime.now(),
  }

class RegisterAPIView(views.APIView):

  def post(self, request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data)

class LoginAPIView(views.APIView):

  def post(self, request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()

    if user is None:
      raise exceptions.AuthenticationFailed("User does not exist")

    if not user.check_password(password):
      raise exceptions.AuthenticationFailed("Incorrect password")

    payload = create_payload(user)

    access_token = jwt.encode(payload, 'SECRET', algorithm='HS256')
    refresh_token = jwt.encode({'id': user.id}, 'SECRET', algorithm='HS256')

    response = Response()

    response.set_cookie(key='access_token', value=access_token, httponly=True, max_age=20)
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

    return response

class UserAPIView(views.APIView):

  def get(self, request):
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
      raise exceptions.AuthenticationFailed('Non authenticated')

    try:
      payload = jwt.decode(refresh_token, 'SECRET', algorithms=['HS256'])

      user = User.objects.filter(id=payload['id']).first()

      payload = create_payload(user)

      access_token = jwt.encode(payload, 'SECRET', algorithm='HS256')

      serializer = UserSerializer(user)

      response = Response(serializer.data)
      response.set_cookie(key='access_token', value=access_token, httponly=True, max_age=20)

      return response
    except:
      raise exceptions.AuthenticationFailed('Non authenticated')

class LogoutAPIView(views.APIView):

  def post(self, request):
    response = Response({'message': 'Success'})

    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response
