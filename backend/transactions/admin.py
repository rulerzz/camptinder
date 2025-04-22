from django.contrib import admin
from .models import VippsCredentials, Coupon
from backend.admin_sites import main_admin_site, org_admin_site
# Register your models here.


class VippsCredentialsAdmin(admin.ModelAdmin):
    list_display = ('organization', 'environment', 'is_active')
    list_filter = ('environment', 'is_active')
    search_fields = ('organization__name', 'merchant_serial_number')
    readonly_fields = ('client_id', 'client_secret', 'subscription_key')
try:
    main_admin_site.unregister(VippsCredentials)
except admin.sites.NotRegistered:
    pass

main_admin_site.register(VippsCredentials)


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'organization', 'discount_type', 'discount_value', 'is_active', 'valid_from', 'valid_until', 'used_count', 'max_uses')
    list_filter = ('discount_type', 'is_active', 'organization')
    search_fields = ('code', 'organization__name')
    readonly_fields = ('used_count',)

try:
    main_admin_site.unregister(Coupon)
except admin.sites.NotRegistered:
    pass

main_admin_site.register(Coupon)

