from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

class MainAdminSite(AdminSite):
    """Main admin site for system administrators."""
    site_header = _("System Administration")
    site_title = _("System Admin Portal")
    index_title = _("System Management")
    
    def has_permission(self, request):
        """
        Restrict access to the main admin site to superusers only.
        Organization staff can't access the main admin.
        """
        if not hasattr(request, 'user') or not request.user.is_authenticated or not request.user.is_active:
            return False
            
        # Only superusers can access the main admin, regardless of staff status
        if request.user.is_superuser:
            return True
            
        # Check if user is a member of any organization
        # If so, they should use the org admin instead
        if hasattr(request.user, 'organization_memberships') and request.user.organization_memberships.exists():
            return False
            
        # Allow staff users who are not organization members
        return request.user.is_staff

class OrganizationAdminSite(AdminSite):
    """Organization-specific admin site."""
    site_header = _("Organization Administration")
    site_title = _("Organization Portal")
    index_title = _("Organization Management")
    login_template = 'admin/org_login.html'
    index_template = 'admin/org_index.html'
    
    def has_permission(self, request):
        """
        Check if the user has access to the organization admin.
        """
        # First check if user attribute exists and user is authenticated and active
        if not hasattr(request, 'user') or not request.user.is_authenticated or not request.user.is_active:
            return False
        
        # Check if the user is a superuser (superusers can access everything)
        if request.user.is_superuser:
            return True
        
        # Staff check - required for Django admin access
        if not request.user.is_staff:
            return False
            
        # Check if user has an organization membership with appropriate role
        if hasattr(request.user, 'organization_memberships'):
            active_memberships = request.user.organization_memberships.filter(
                is_active=True,
                role__in=['ADMIN', 'MANAGER', 'STAFF', 'TECHNICIAN']
            )
            return active_memberships.exists()
            
        return False

# Instantiate the admin sites
main_admin_site = MainAdminSite(name='main_admin')
org_admin_site = OrganizationAdminSite(name='org_admin')