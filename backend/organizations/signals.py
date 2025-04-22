from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import OrganizationUser

try:
    @receiver(post_save, sender=OrganizationUser)
    def assign_group_based_on_role(sender, instance, created, **kwargs):
        """
        When an OrganizationUser is saved, assign the appropriate Django group
        based on the role and update staff status.
        """

        role_to_group = {
            'ADMIN': 'Organization Admin',
            'MANAGER': 'Organization Manager',
            'STAFF': 'Organization Staff',
            'TECHNICIAN': 'Machine Technician',
            'VIEWER': 'Read-Only User',
        }
        
        staff_roles = ['ADMIN', 'MANAGER', 'STAFF', 'TECHNICIAN']
        
        group_name = role_to_group.get(instance.role)
        if not group_name:
            return
        
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            print(f"Group {group_name} doesn't exist. Please run setup_groups command.")
            return
        
        for role_group in role_to_group.values():
            try:
                g = Group.objects.get(name=role_group)
                instance.user.groups.remove(g)
            except Group.DoesNotExist:
                pass

        instance.user.groups.add(group)
        
        #Special handling for staff status
        if instance.role in staff_roles and instance.is_active:
            instance.user.is_staff = True
        else:
            has_staff_role = OrganizationUser.objects.filter(
                user=instance.user, 
                role__in=staff_roles,
                is_active=True
            ).exclude(id=instance.id).exists()
            
            if not has_staff_role:
                instance.user.is_staff = False
        
        if not instance.user.is_superuser:
            instance.user.is_superuser = False
            
        if hasattr(instance.user, '_original_is_staff'):
            if instance.user.is_staff != instance.user._original_is_staff:
                instance.user.save(update_fields=['is_staff', 'is_superuser'])
        else:
            instance.user.save(update_fields=['is_staff', 'is_superuser'])
except Exception as e:
    print(f"Error in organization signals: {e}")