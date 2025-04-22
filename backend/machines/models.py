from django.db import models
from django.db.models import Count, Q
from locations.models import Location
from organizations.models import Organization, OrganizationUser
from core.models import User

class Machine(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    battery_level = models.IntegerField(null=True, blank=True)
    alarm_battery_level = models.IntegerField(null=True, blank=True)
    temp_level = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    last_maintenance = models.DateField(null=True, blank=True)
    production_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    area_code = models.CharField(max_length=20, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['area_code', 'serial_number'], name='uq_area_code_serial_number')
        ]
    
    def save(self, *args, **kwargs):
        if self.location and not self.area_code:
            self.area_code = self.location.area_code
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.serial_number
    
    def get_variant_inventory(self):
        from inventory.models import Locker 
        return (self.lockers.filter(
            state=Locker.AVAILABLE,
            product_variant__isnull=False
        ).values(
            'product_variant__id',
            'product_variant__product__name',
            'product_variant__size',
            'product_variant__price'
        ).annotate(
            available=Count('id')
        ).order_by('product_variant__product__name', 'product_variant__size'))