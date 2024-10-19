import jwt
from rest_framework import exceptions

from ..models import User


def user_session_exists(request):
    return request.user is not None and not request.user.is_anonymous


def get_user(request):
    access_token = request.COOKIES.get("access_token")

    if user_session_exists(request):
        return request.user

    try:
        payload = jwt.decode(access_token, "SECRET", algorithms=["HS256"])

        user = User.objects.filter(id=payload["id"]).first()

        return user
    except:
        raise exceptions.AuthenticationFailed("Unauthenticated")
