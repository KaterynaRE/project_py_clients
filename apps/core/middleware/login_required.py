from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve

EXEMPT_URLS = [
    'admin:login',
    'admin:logout',
    'admin:index',
    'core:about_project',
    'login',
    'logout',
    'register',
    'core:welcome',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resolver_match = resolve(request.path)
        # view_name включає namespace
        view_name = resolver_match.view_name
        # Якщо адреса дозволена без аутентифікації
        if view_name in EXEMPT_URLS:
            return self.get_response(request)
        # Якщо користувач не аутентифікований
        if not request.user.is_authenticated:
            return redirect('core:welcome')
        # Якщо користувач аутентифікований
        # і адреса не дозволена без аутентифікації
        return self.get_response(request)


class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            resolver_match = resolve(request.path)
            view_name = resolver_match.view_name

            # Якщо адмін – може увійти на будь-яку адресу
            if request.user.role == 'admin':
                return self.get_response(request)
            # На сторінку users може увійти тільки адмін
            elif view_name == 'users' and request.user.role != 'admin':
                return redirect('core:home')
            # Якщо гість – може увійти на адресу 'core:about_core'
            # або на EXEMPT_URLS
            elif request.user.role == 'guest':
                if view_name == 'core:about_core' or view_name in EXEMPT_URLS:
                    return self.get_response(request)
                return redirect('core:about_core')

        return self.get_response(request)
