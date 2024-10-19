import re

from django.shortcuts import redirect

SHOULD_NOT_BE_LOGGED_IN = ["/accounts/login/", "/accounts/register/", "/admin/login/"]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if re.match(".*/api/.*", request.path):
            pass
        elif not request.user.is_authenticated and request.path not in SHOULD_NOT_BE_LOGGED_IN:
            return redirect("accounts-login")

        response = self.get_response(request)

        return response
