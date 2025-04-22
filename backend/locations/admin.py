from django.contrib import admin
from .models import Location, Country
from backend.admin_sites import main_admin_site, org_admin_site
from machines.models import Machine

class MainCountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_code')
    search_fields = ('country_name', 'country_code')

try:
    main_admin_site.unregister(Country)
except admin.sites.NotRegistered:
    pass
main_admin_site.register(Country, MainCountryAdmin)

class MainLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')

try:
    main_admin_site.unregister(Location)
except admin.sites.NotRegistered:
    pass
main_admin_site.register(Location, MainLocationAdmin)


class OrganizationCountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_code')
    search_fields = ('country_name', 'country_code')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
            
        if hasattr(request.user, 'organization_memberships'):
            org_ids = request.user.organization_memberships.filter(
                is_active=True
            ).values_list('organization_id', flat=True)
            
            machine_location_ids = Machine.objects.filter(
                organization_id__in=org_ids
            ).values_list('location_id', flat=True).distinct()
            
            return qs.filter(id__in=machine_location_ids)
        
        return qs.none()
    
try:
    org_admin_site.unregister(Country)
except admin.sites.NotRegistered:
    pass
org_admin_site.register(Country, OrganizationCountryAdmin)

class OrganizationLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
            
        if hasattr(request.user, 'organization_memberships'):
            org_ids = request.user.organization_memberships.filter(
                is_active=True
            ).values_list('organization_id', flat=True)
            
            machine_location_ids = Machine.objects.filter(
                organization_id__in=org_ids
            ).values_list('location_id', flat=True).distinct()
            
            return qs.filter(id__in=machine_location_ids)
        
        return qs.none()
    
try:
    org_admin_site.unregister(Location)
except admin.sites.NotRegistered:
    pass
org_admin_site.register(Location, OrganizationLocationAdmin)