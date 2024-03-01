from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


ALLOWED_ROLES = ['GA', 'Accounting', 'Admin']

def has_allowed_role(user):
    return user.groups.filter(name__in=ALLOWED_ROLES).exists()

def allowed_roles_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not has_allowed_role(request.user):
            return redirect( '/forbidden')
        return view_func(request, *args, **kwargs)
    return wrapper

