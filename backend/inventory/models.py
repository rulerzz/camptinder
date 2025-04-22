from django.db import models
from machines.models import Machine

class ProductType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
   
    class Meta:
        verbose_name_plural = "Product Categories"
   
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True, null=True)
    hazardous = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('product', 'sku')
    
    def __str__(self):
        size_str = f" - {self.size}" if self.size else ""
        return f"{self.product.name}{size_str} (${self.price})"
        
    def get_available_count(self):
        return self.lockers.filter(state=Locker.AVAILABLE).count()

class LockerType(models.Model):
    size = models.CharField(max_length=25)
    description = models.TextField(blank=True, null=True)
   
    def __str__(self):
        return self.size

class Locker(models.Model):
    AVAILABLE = 'Available'
    EMPTY = 'Empty'
    RENTED = 'Rented'
    BROKEN = 'Broken'
    IN_MAINTENANCE = 'In Maintenance'
   
    STATE_CHOICES = [
        (AVAILABLE, 'Available'),
        (EMPTY, 'Empty'),
        (RENTED, 'Rented'),
        (BROKEN, 'Broken'),
        (IN_MAINTENANCE, 'In Maintenance')
    ]
   
    identifier = models.CharField(max_length=50)
    type = models.ForeignKey(LockerType, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='lockers')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='lockers')
    easy_access = models.BooleanField(default=False)
    state = models.CharField(max_length=50, choices=STATE_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return f"{self.identifier} ({self.machine.name})"
   
    class Meta:
        unique_together = ('machine', 'identifier')

class MachineInventory(Machine):
    class Meta:
        proxy = True
        verbose_name = "Machine Inventory"
        verbose_name_plural = "Machine Inventories"
    