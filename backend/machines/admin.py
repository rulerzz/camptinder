from django.contrib import admin
from .models import Machine
from backend.admin_sites import main_admin_site, org_admin_site
from organizations.models import Organization

class MainMachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'location', 'organization', 'is_active', 'battery_level')
    list_filter = ('is_active', 'organization', 'location')
    search_fields = ('name', 'serial_number', 'area_code')
    readonly_fields = ('created_at', 'updated_at')

try:
    main_admin_site.unregister(Machine)
except admin.sites.NotRegistered:
    pass
main_admin_site.register(Machine, MainMachineAdmin)

class OrganizationMachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'location', 'is_active', 'battery_level')
    list_filter = ('is_active', 'location')
    search_fields = ('name', 'serial_number', 'area_code')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
            
        if hasattr(request.user, 'organization_memberships'):
            org_ids = request.user.organization_memberships.filter(
                is_active=True
            ).values_list('organization_id', flat=True)
            
            return qs.filter(organization_id__in=org_ids)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization":
            if not request.user.is_superuser and hasattr(request.user, 'organization_memberships'):
                org_ids = request.user.organization_memberships.filter(
                    is_active=True
                ).values_list('organization_id', flat=True)
                
                kwargs["queryset"] = Organization.objects.filter(id__in=org_ids)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:
            if not obj.organization_id and not request.user.is_superuser and hasattr(request.user, 'organization_memberships'):
                org_membership = request.user.organization_memberships.filter(is_active=True).first()
                if org_membership:
                    obj.organization = org_membership.organization
        
        super().save_model(request, obj, form, change)

try:
    org_admin_site.unregister(Machine)
except admin.sites.NotRegistered:
    pass
org_admin_site.register(Machine, OrganizationMachineAdmin)