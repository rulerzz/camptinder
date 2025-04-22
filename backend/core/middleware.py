from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        if hasattr(request, 'user') and request.user.is_authenticated:
        
            if request.path.startswith('/admin/'):
                if 'login' in request.path or '/static/' in request.path:
                    return response
                    
                if request.user.is_superuser:
                    return response
                    
                if hasattr(request.user, 'organization_memberships'):
                    if request.user.organization_memberships.filter(is_active=True).exists():
                        return redirect('/org-admin/')
            
            if request.path.startswith('/org-admin/'):
                if 'login' in request.path or '/static/' in request.path:
                    return response
                    
                if request.user.is_superuser:
                    return response
                
                if not request.user.is_staff:
                    return redirect('/org-admin/login/?next=/org-admin/')
                    
                if hasattr(request.user, 'organization_memberships'):
                    has_active_membership = request.user.organization_memberships.filter(
                        is_active=True,
                        role__in=['ADMIN', 'MANAGER', 'STAFF', 'TECHNICIAN']
                    ).exists()
                    
                    if not has_active_membership:
                        return redirect('/org-admin/login/?next=/org-admin/')
                else:
                    return redirect('/org-admin/login/?next=/org-admin/')
        
        return response