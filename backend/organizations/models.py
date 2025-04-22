from django.db import models
from core.models import User

class Organization(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class OrganizationUser(models.Model):
    
    ROLE_CHOICES = (
        ('ADMIN', 'Organization Admin'),
        ('MANAGER', 'Organization Manager'),
        ('STAFF', 'Organization Staff'),
        ('TECHNICIAN', 'Machine Technician'),
        ('VIEWER', 'Read-Only User'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organization_memberships')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='STAFF')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    can_view_all_machines = models.BooleanField(default=False, help_text="Can view all machines in the organization regardless of assignment")
    can_edit_all_machines = models.BooleanField(default=False, help_text="Can edit all machines in the organization regardless of assignment")
    can_manage_users = models.BooleanField(default=False, help_text="Can manage users in this organization")
    
    class Meta:
        unique_together = ('user', 'organization')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.user} - {self.organization} ({self.get_role_display()})"
        
    def save(self, *args, **kwargs):
        if self.role == 'ADMIN':
            self.can_view_all_machines = True
            self.can_edit_all_machines = True
            self.can_manage_users = True
        elif self.role == 'MANAGER':
            self.can_view_all_machines = True
            self.can_edit_all_machines = True
            self.can_manage_users = True
        elif self.role == 'STAFF':
            self.can_view_all_machines = True
            self.can_edit_all_machines = False
            self.can_manage_users = False
        elif self.role == 'TECHNICIAN':
            self.can_view_all_machines = True
            self.can_edit_all_machines = True
            self.can_manage_users = False
        elif self.role == 'VIEWER':
            self.can_view_all_machines = True
            self.can_edit_all_machines = False
            self.can_manage_users = False
        
        if self.is_active and self.role in ['ADMIN', 'MANAGER', 'STAFF', 'TECHNICIAN']:
            self.user.is_staff = True
            self.user.save(update_fields=['is_staff'])
        
        super().save(*args, **kwargs)