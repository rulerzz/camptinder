from django.contrib import admin
from .models import Organization, OrganizationUser
from backend.admin_sites import main_admin_site, org_admin_site

class OrganizationUserInline(admin.TabularInline):
    model = OrganizationUser
    extra = 1
    fk_name = 'organization'

class MainOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'contact_email', 'is_active')
    search_fields = ('name', 'code', 'contact_email')
    list_filter = ('is_active',)
    inlines = [OrganizationUserInline]
    
class MainOrganizationUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'is_active')
    list_filter = ('organization', 'role', 'is_active')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')

try:
    main_admin_site.unregister(Organization)
except admin.sites.NotRegistered:
    pass
main_admin_site.register(Organization, MainOrganizationAdmin)

try:
    main_admin_site.unregister(OrganizationUser)
except admin.sites.NotRegistered:
    pass
main_admin_site.register(OrganizationUser, MainOrganizationUserAdmin)

class OrgAdminOrganizationAdmin(admin.ModelAdmin):
    """Organization admin for organization users."""
    list_display = ('name', 'code', 'contact_email')
    readonly_fields = ('name', 'code', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        """Only show the organizations the user belongs to."""
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
            
        if hasattr(request.user, 'organization_memberships'):
            org_ids = request.user.organization_memberships.filter(
                is_active=True
            ).values_list('organization_id', flat=True)
            
            return qs.filter(id__in=org_ids)
        
        return qs.none()
    
    def has_add_permission(self, request):
        """Organizations can't create new organizations."""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Organizations can't delete organizations."""
        return request.user.is_superuser

class OrgAdminOrganizationUserAdmin(admin.ModelAdmin):
    """OrganizationUser admin for organization admins."""
    list_display = ('user', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    
    def get_queryset(self, request):
        """Only show users from the current user's organizations."""
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
            
        if hasattr(request.user, 'organization_memberships'):
            org_ids = request.user.organization_memberships.filter(
                is_active=True
            ).values_list('organization_id', flat=True)
            
            can_manage = request.user.organization_memberships.filter(
                is_active=True,
                can_manage_users=True
            ).exists()
            
            if can_manage:
                return qs.filter(organization_id__in=org_ids)
            else:
                return qs.filter(user=request.user)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit organization choices to those the user belongs to."""
        if db_field.name == "organization":
            if not request.user.is_superuser and hasattr(request.user, 'organization_memberships'):
                org_ids = request.user.organization_memberships.filter(
                    is_active=True,
                    can_manage_users=True
                ).values_list('organization_id', flat=True)
                
                kwargs["queryset"] = Organization.objects.filter(id__in=org_ids)
                
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
try:
    org_admin_site.unregister(Organization)
except admin.sites.NotRegistered:
    pass
org_admin_site.register(Organization, OrgAdminOrganizationAdmin)

try:
    org_admin_site.unregister(OrganizationUser)
except admin.sites.NotRegistered:
    pass
org_admin_site.register(OrganizationUser, OrgAdminOrganizationUserAdmin)