from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserRole
from backend.admin_sites import main_admin_site, org_admin_site

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'description', 'created_at')
    search_fields = ('role_name', 'description')

try:
    main_admin_site.unregister(UserRole)
except admin.sites.NotRegistered:
    pass
main_admin_site.register(UserRole, UserRoleAdmin)

class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'role',
                       'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'role')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)
    list_filter = ('is_active', 'is_staff', 'role')

try:
    main_admin_site.unregister(User)
except admin.sites.NotRegistered:
    pass
main_admin_site.register(User, UserAdmin)

class OrgAdminUserAdmin(DjangoUserAdmin):
    """User admin for organization admins to manage users."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Organization settings'), {'fields': ('is_active', 'is_verified')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('email',)
    list_filter = ('is_active',)
    
    def get_queryset(self, request):
        """
        Only show users who are members of the organization(s) that the 
        current user has management rights for.
        """
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
            
        if hasattr(request.user, 'organization_memberships'):
            managed_orgs = request.user.organization_memberships.filter(
                is_active=True,
                can_manage_users=True
            ).values_list('organization_id', flat=True)
            
            from organizations.models import OrganizationUser
            managed_user_ids = OrganizationUser.objects.filter(
                organization_id__in=managed_orgs
            ).values_list('user_id', flat=True)
            
            return qs.filter(id__in=managed_user_ids)
        
        return qs.none()
    
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
            
        if hasattr(request.user, 'organization_memberships'):
            return request.user.organization_memberships.filter(
                is_active=True, 
                can_manage_users=True
            ).exists()
        return False

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.is_staff = False
            obj.is_superuser = False
        
        # Save the user
        super().save_model(request, obj, form, change)
        
        if not change:  #Only for new users
            if not request.user.is_superuser and hasattr(request.user, 'organization_memberships'):
                from organizations.models import OrganizationUser
                admin_membership = request.user.organization_memberships.filter(
                    is_active=True,
                    can_manage_users=True
                ).first()
                
                if admin_membership:
                    OrganizationUser.objects.create(
                        user=obj,
                        organization=admin_membership.organization,
                        role='STAFF'  # Default role
                    )

try:
    org_admin_site.unregister(User)
except admin.sites.NotRegistered:
    pass
org_admin_site.register(User, OrgAdminUserAdmin)


from django.contrib.admin.models import LogEntry

@admin.register(LogEntry, site=main_admin_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    list_filter = ('user', 'content_type', 'action_flag')
    search_fields = ('object_repr',)