from django.shortcuts import redirect


ALLOWED_ROLES_1 = ['GA', 'Admin']
ALLOWED_ROLES_2 = ['GA', 'Accounting', 'Admin']
ALLOWED_ROLES_3 = ['Admin', 'Messenger', 'FO']
ALLOWED_ROLES_4= ['Admin', 'FO']
ALLOWED_ROLES_5= ['Admin']

def has_allowed_role1(user):
    return user.groups.filter(name__in=ALLOWED_ROLES_1).exists()

def has_allowed_role2(user):
    return user.groups.filter(name__in=ALLOWED_ROLES_2).exists()

def has_allowed_role3(user):
    return user.groups.filter(name__in=ALLOWED_ROLES_3).exists()

def has_allowed_role4(user):
    return user.groups.filter(name__in=ALLOWED_ROLES_4).exists()

def has_allowed_role5(user):
    return user.groups.filter(name__in=ALLOWED_ROLES_5).exists()

def GA_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not has_allowed_role1(request.user):
            return redirect( '/forbidden')
        return view_func(request, *args, **kwargs)
    return wrapper

def Messenger_Forbidden(view_func):
    def wrapper(request, *args, **kwargs):
        if not has_allowed_role2(request.user):
            return redirect( '/forbidden')
        return view_func(request, *args, **kwargs)
    return wrapper

def Messenger_Only(view_func):
    def wrapper(request, *args, **kwargs):
        if not has_allowed_role3(request.user):
            return redirect('/forbidden')
        return view_func(request, *args, **kwargs)
    return wrapper

def FO_Only(view_func):
    def wrapper(request, *args, **kwargs):
        if not has_allowed_role4(request.user):
            return redirect('/forbidden')
        return view_func(request, *args, **kwargs)
    return wrapper

def Admin_Only(view_func):
    def wrapper(request, *args, **kwargs):
        if not has_allowed_role5(request.user):
            return redirect('/forbidden')
        return view_func(request, *args, **kwargs)
    return wrapper