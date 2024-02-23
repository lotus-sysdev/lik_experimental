# myapp/decorators.py
from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return wrapper

def manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Manager').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return wrapper


