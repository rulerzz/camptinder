from django.db import models
from django.utils import timezone
from decimal import Decimal

class VippsCredentials(models.Model):

    ENVIRONMENT_CHOICES = [
        ('test', 'Test Environment'),
        ('production', 'Production Environment'),
    ]

    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    environment = models.CharField(max_length=10, choices=ENVIRONMENT_CHOICES, default='test')
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=225)
    subscription_key = models.CharField(max_length=100)
    merchant_serial_number = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('organization', 'environment')
        verbose_name = "Vipps Credential"
        verbose_name_plural = "Vipps Credentials"
        app_label = 'transactions'

    def __str__(self):
        return f"{self.organization.name} - {self.get_environment_display()}"

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=10, choices=[
        ('percent', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.ForeignKey('inventory.ProductType', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('inventory.Product', on_delete=models.SET_NULL, null=True, blank=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(null=True, blank=True)
    max_uses = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.code} - {self.get_discount_display()}"

    def get_discount_display(self):
        if self.discount_type == 'percent':
            return f"{self.discount_value}%"
        return f"${self.discount_value}"

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.used_count < self.max_uses and
            (self.valid_until is None or self.valid_until > now)
        )

    def apply_discount(self, amount):
        if self.discount_type == 'percent':
            return amount * (Decimal('1.0') - (self.discount_value / Decimal('100.0')))
        else:
            return max(Decimal('0'), amount - self.discount_value)