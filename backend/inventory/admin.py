from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import ProductType, Product, ProductVariant, LockerType, Locker
from backend.admin_sites import main_admin_site, org_admin_site
from organizations.models import Organization

#Main Admin Site Classes
class MainProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('sku', 'size', 'price', 'deposit', 'expiry_date', 'is_active')

class MainProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'organization', 'variants_count', 'hazardous')
    list_filter = ('type', 'hazardous', 'organization')
    search_fields = ('name', 'description')
    inlines = [ProductVariantInline]
    
    def variants_count(self, obj):
        return obj.variants.count()
    variants_count.short_description = 'Variants'

class MainProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'size', 'price', 'deposit', 'expiry_date', 'is_active', 'available_count')
    list_filter = ('product__type', 'is_active', 'product__organization')
    search_fields = ('product__name', 'sku', 'size')
    autocomplete_fields = ('product',)
    
    def available_count(self, obj):
        return obj.get_available_count()
    available_count.short_description = 'Available'

class MainLockerTypeAdmin(admin.ModelAdmin):
    list_display = ('size', 'description')
    search_fields = ('size', 'description')

class MainLockerAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'machine', 'product_variant_display', 'type', 'state', 'easy_access')
    list_filter = ('machine', 'type', 'state', 'easy_access')
    search_fields = ('identifier', 'product_variant__product__name')
    autocomplete_fields = ('machine', 'type', 'product_variant')
    
    def product_variant_display(self, obj):
        if obj.product_variant:
            return f"{obj.product_variant.product.name} - {obj.product_variant.size} (${obj.product_variant.price})"
        return "-"
    product_variant_display.short_description = 'Product'

class LockerInline(admin.TabularInline):
    model = Locker
    fields = ('identifier', 'product_variant', 'type', 'state')
    extra = 0
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('product_variant', 'product_variant__product', 'type')

class MainMachineInventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'location', 'organization', 'inventory_summary', 'is_active')
    list_filter = ('organization', 'location', 'is_active')
    search_fields = ('name', 'serial_number')
    readonly_fields = ('created_at', 'updated_at', 'inventory_detail')
    inlines = [LockerInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'serial_number', 'organization', 'location', 'is_active')
        }),
        ('Device Information', {
            'fields': ('battery_level', 'alarm_battery_level', 'temp_level', 'last_maintenance')
        }),
        ('Inventory Summary', {
            'fields': ('inventory_detail',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'area_code')
        }),
    )
    
    def get_queryset(self, request):
        from machines.models import Machine
        return Machine.objects.all().prefetch_related(
            'lockers', 
            'lockers__product_variant', 
            'lockers__product_variant__product'
        )
    
    def inventory_summary(self, obj):
        inventory = obj.get_variant_inventory()
        summary_parts = [
            f"{item['product_variant__product__name']} {item['product_variant__size']}: {item['available']}" 
            for item in inventory
        ]
        return ", ".join(summary_parts) if summary_parts else "No inventory"
    
    inventory_summary.short_description = "Inventory"
    
    def inventory_detail(self, obj):
        inventory = obj.get_variant_inventory()
        if not inventory:
            return "No inventory data available"
            
        html = '<table class="inventory-table"><tr><th>Product</th><th>Size</th><th>Price</th><th>Available</th></tr>'
        for item in inventory:
            html += f"""
            <tr>
                <td>{item['product_variant__product__name']}</td>
                <td>{item['product_variant__size'] or '-'}</td>
                <td>${item['product_variant__price']}</td>
                <td>{item['available']}</td>
            </tr>
            """
        html += '</table>'
        return format_html(html)
    
    inventory_detail.short_description = "Detailed Inventory"
    
    class Media:
        css = {
            'all': ('admin/css/inventory.css',)
        }

for model, admin_class in [
    (ProductType, MainProductTypeAdmin),
    (Product, MainProductAdmin),
    (ProductVariant, MainProductVariantAdmin),
    (LockerType, MainLockerTypeAdmin),
    (Locker, MainLockerAdmin),
]:
    try:
        main_admin_site.unregister(model)
    except admin.sites.NotRegistered:
        pass
    main_admin_site.register(model, admin_class)

try:
    from .models import MachineInventory
    try:
        main_admin_site.unregister(MachineInventory)
    except admin.sites.NotRegistered:
        pass
    main_admin_site.register(MachineInventory, MainMachineInventoryAdmin)
except ImportError:
    try:
        from machines.models import Machine
        try:
            main_admin_site.unregister(Machine)
        except admin.sites.NotRegistered:
            pass
        main_admin_site.register(Machine, MainMachineInventoryAdmin)
    except:
        pass

#Organization Admin Site Classes
class OrgProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class OrgProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('sku', 'size', 'price', 'deposit', 'expiry_date', 'is_active')

class OrgProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'variants_count', 'hazardous')
    list_filter = ('type', 'hazardous')
    search_fields = ('name', 'description')
    inlines = [OrgProductVariantInline]
    
    def variants_count(self, obj):
        return obj.variants.count()
    variants_count.short_description = 'Variants'
    
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

class OrgProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'size', 'price', 'deposit', 'expiry_date', 'is_active', 'available_count')
    list_filter = ('product__type', 'is_active')
    search_fields = ('product__name', 'sku', 'size')
    autocomplete_fields = ('product',)
    
    def available_count(self, obj):
        return obj.get_available_count()
    available_count.short_description = 'Available'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
            
        if hasattr(request.user, 'organization_memberships'):
            org_ids = request.user.organization_memberships.filter(
                is_active=True
            ).values_list('organization_id', flat=True)
            
            return qs.filter(product__organization_id__in=org_ids)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            if not request.user.is_superuser and hasattr(request.user, 'organization_memberships'):
                org_ids = request.user.organization_memberships.filter(
                    is_active=True
                ).values_list('organization_id', flat=True)
                
                kwargs["queryset"] = Product.objects.filter(organization_id__in=org_ids)
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrgLockerTypeAdmin(admin.ModelAdmin):
    list_display = ('size', 'description')
    search_fields = ('size', 'description')

class OrgLockerAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'machine', 'product_variant_display', 'type', 'state', 'easy_access')
    list_filter = ('machine', 'type', 'state', 'easy_access')
    search_fields = ('identifier', 'product_variant__product__name')
    autocomplete_fields = ('machine', 'type', 'product_variant')
    
    def product_variant_display(self, obj):
        if obj.product_variant:
            return f"{obj.product_variant.product.name} - {obj.product_variant.size} (${obj.product_variant.price})"
        return "-"
    product_variant_display.short_description = 'Product'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related(
            'product_variant', 'product_variant__product', 'machine', 'type'
        )
        
        if request.user.is_superuser:
            return qs
            
        if hasattr(request.user, 'organization_memberships'):
            org_ids = request.user.organization_memberships.filter(
                is_active=True
            ).values_list('organization_id', flat=True)
            
            return qs.filter(machine__organization_id__in=org_ids)
        
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_memberships'):
            org_ids = request.user.organization_memberships.filter(
                is_active=True
            ).values_list('organization_id', flat=True)
            
            if db_field.name == "machine":
                kwargs["queryset"] = Machine.objects.filter(organization_id__in=org_ids)
            
            elif db_field.name == "product_variant":
                kwargs["queryset"] = ProductVariant.objects.filter(
                    product__organization_id__in=org_ids
                ).select_related('product')
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrgLockerInline(admin.TabularInline):
    model = Locker
    fields = ('identifier', 'product_variant', 'type', 'state')
    extra = 0
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('product_variant', 'product_variant__product', 'type')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'organization_memberships'):
            org_ids = request.user.organization_memberships.filter(
                is_active=True
            ).values_list('organization_id', flat=True)
            
            if db_field.name == "product_variant":
                kwargs["queryset"] = ProductVariant.objects.filter(
                    product__organization_id__in=org_ids
                ).select_related('product')
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrgMachineInventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'location', 'inventory_summary', 'is_active')
    list_filter = ('location', 'is_active')
    search_fields = ('name', 'serial_number')
    readonly_fields = ('created_at', 'updated_at', 'inventory_detail')
    inlines = [OrgLockerInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'serial_number', 'location', 'is_active')
        }),
        ('Device Information', {
            'fields': ('battery_level', 'alarm_battery_level', 'temp_level', 'last_maintenance')
        }),
        ('Inventory Summary', {
            'fields': ('inventory_detail',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'area_code')
        }),
    )
    
    def get_queryset(self, request):
        from machines.models import Machine
        qs = Machine.objects.all().prefetch_related(
            'lockers', 
            'lockers__product_variant', 
            'lockers__product_variant__product'
        )
        
        if request.user.is_superuser:
            return qs
            
        if hasattr(request.user, 'organization_memberships'):
            org_ids = request.user.organization_memberships.filter(
                is_active=True
            ).values_list('organization_id', flat=True)
            
            return qs.filter(organization_id__in=org_ids)
        
        return qs.none()
    
    def inventory_summary(self, obj):
        inventory = obj.get_variant_inventory()
        summary_parts = [
            f"{item['product_variant__product__name']} {item['product_variant__size']}: {item['available']}" 
            for item in inventory
        ]
        return ", ".join(summary_parts) if summary_parts else "No inventory"
    
    inventory_summary.short_description = "Inventory"
    
    def inventory_detail(self, obj):
        inventory = obj.get_variant_inventory()
        if not inventory:
            return "No inventory data available"
            
        html = '<table class="inventory-table"><tr><th>Product</th><th>Size</th><th>Price</th><th>Available</th></tr>'
        for item in inventory:
            html += f"""
            <tr>
                <td>{item['product_variant__product__name']}</td>
                <td>{item['product_variant__size'] or '-'}</td>
                <td>${item['product_variant__price']}</td>
                <td>{item['available']}</td>
            </tr>
            """
        html += '</table>'
        return format_html(html)
    
    inventory_detail.short_description = "Detailed Inventory"

for model, admin_class in [
    (ProductType, OrgProductTypeAdmin),
    (Product, OrgProductAdmin),
    (ProductVariant, OrgProductVariantAdmin),
    (LockerType, OrgLockerTypeAdmin),
    (Locker, OrgLockerAdmin),
]:
    try:
        org_admin_site.unregister(model)
    except admin.sites.NotRegistered:
        pass
    org_admin_site.register(model, admin_class)

try:
    from .models import MachineInventory
    try:
        org_admin_site.unregister(MachineInventory)
    except admin.sites.NotRegistered:
        pass
    org_admin_site.register(MachineInventory, OrgMachineInventoryAdmin)
except ImportError:
    try:
        from machines.models import Machine
        try:
            org_admin_site.unregister(Machine)
        except admin.sites.NotRegistered:
            pass
        org_admin_site.register(Machine, OrgMachineInventoryAdmin)
    except:
        pass