from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def group_required(group_name):
    def in_groups(user):
        if user.is_superuser:
            return True
        return user.groups.filter(name=group_name).exists()
    
    return user_passes_test(in_groups, login_url=None, redirect_field_name=None)

def organization_admin_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_superuser or u.groups.filter(name='Organization Admin').exists(),
        login_url=None
    )(view_func)
    return decorated_view_func

def organization_role_required(allowed_roles):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            if hasattr(request.user, 'organization_memberships'):
                has_role = request.user.organization_memberships.filter(
                    is_active=True,
                    role__in=allowed_roles
                ).exists()
                
                if has_role:
                    return view_func(request, *args, **kwargs)
                    
            return HttpResponseForbidden("You don't have permission to access this page.")
        return wrapped_view
    return decorator