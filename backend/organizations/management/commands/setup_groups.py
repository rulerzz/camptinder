from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from machines.models import Machine
from organizations.models import Organization, OrganizationUser
from locations.models import Location
from core.models import User
from inventory.models import ProductType, ProductVariant, Product, LockerType, Locker, MachineInventory

class Command(BaseCommand):
    help = 'Set up initial groups and permissions'

    def handle(self, *args, **options):
        #Create groups
        groups = {
            'Organization Admin': Group.objects.get_or_create(name='Organization Admin')[0],
            'Organization Manager': Group.objects.get_or_create(name='Organization Manager')[0],
            'Organization Staff': Group.objects.get_or_create(name='Organization Staff')[0],
            'Machine Technician': Group.objects.get_or_create(name='Machine Technician')[0],
            'Read-Only User': Group.objects.get_or_create(name='Read-Only User')[0],
        }

        #Clear existing permissions
        for group in groups.values():
            group.permissions.clear()

        #Get content types
        machine_ct = ContentType.objects.get_for_model(Machine)
        machineinv_ct = ContentType.objects.get(app_label='inventory', model='machineinventory')
        organization_ct = ContentType.objects.get_for_model(Organization)
        org_user_ct = ContentType.objects.get_for_model(OrganizationUser)
        location_ct = ContentType.objects.get_for_model(Location)
        user_ct = ContentType.objects.get_for_model(User)
        product_type_ct = ContentType.objects.get_for_model(ProductType)
        product_variant_ct = ContentType.objects.get_for_model(ProductVariant)
        product_ct = ContentType.objects.get_for_model(Product)
        locker_type_ct = ContentType.objects.get_for_model(LockerType)
        locker_ct = ContentType.objects.get_for_model(Locker)

        #Helper function to safely get permissions
        def get_permission_safe(content_type, codename):
            try:
                return Permission.objects.get(content_type=content_type, codename=codename)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Permission {codename} for {content_type} not found, skipping"))
                return None

        #Collect permissions
        permissions = []
        models_perms = {
            machine_ct: ['view_machine', 'add_machine', 'change_machine', 'delete_machine'],
            machineinv_ct: ['view_machineinventory', 'add_machineinventory', 'change_machineinventory', 'delete_machineinventory'],
            organization_ct: ['view_organization', 'change_organization'],
            org_user_ct: ['view_organizationuser', 'add_organizationuser', 'change_organizationuser', 'delete_organizationuser'],
            location_ct: ['view_location', 'add_location', 'change_location', 'delete_location'],
            user_ct: ['view_user', 'add_user', 'change_user', 'delete_user'],
            product_type_ct: ['view_producttype', 'add_producttype', 'change_producttype', 'delete_producttype'],
            product_variant_ct: ['view_productvariant', 'add_productvariant', 'change_productvariant', 'delete_productvariant'],
            product_ct: ['view_product', 'add_product', 'change_product', 'delete_product'],
            locker_type_ct: ['view_lockertype', 'add_lockertype', 'change_lockertype', 'delete_lockertype'],
            locker_ct: ['view_locker', 'add_locker', 'change_locker', 'delete_locker']
        }

        for content_type, perm_list in models_perms.items():
            for codename in perm_list:
                perm = get_permission_safe(content_type, codename)
                if perm:
                    permissions.append(perm)

        #Define permissions for each group
        group_permissions = {
            'Organization Admin': {perm.codename for perm in permissions},
            'Organization Manager': {
                'view_machine', 'add_machine', 'change_machine', 'delete_machine',
                'view_machineinventory', 'add_machineinventory', 'change_machineinventory', 'delete_machineinventory',
                'view_organization',
                'view_organizationuser', 'add_organizationuser', 'change_organizationuser',
                'view_location', 'add_location', 'change_location',
                'view_user', 'add_user', 'change_user',
                'view_producttype', 'add_producttype', 'change_producttype',
                'view_productvariant', 'add_productvariant', 'change_productvariant', 'delete_productvariant',
                'view_product', 'add_product', 'change_product',
                'view_lockertype', 'add_lockertype', 'change_lockertype',
                'view_locker', 'add_locker', 'change_locker'
            },
            'Organization Staff': {
                'view_machine', 'add_machine',
                'view_machineinventory',
                'view_organization',
                'view_organizationuser',
                'view_location',
                'view_producttype',
                'view_product', 'add_product',
                'view_lockertype',
                'view_locker', 'add_locker', 'change_locker'
            },
            'Machine Technician': {
                'view_machine', 'add_machine', 'change_machine',
                'view_machineinventory', 'change_machineinventory',
                'view_organization',
                'view_organizationuser',
                'view_location',
                'view_producttype',
                'view_product',
                'view_lockertype',
                'view_locker', 'change_locker'
            },
            'Read-Only User': {
                'view_machine', 'view_machineinventory',
                'view_organization',
                'view_organizationuser',
                'view_location',
                'view_producttype',
                'view_product',
                'view_lockertype',
                'view_locker'
            }
        }

        #Assign permissions to groups
        for group_name, codename_set in group_permissions.items():
            group = groups[group_name]
            for perm in permissions:
                if perm.codename in codename_set:
                    group.permissions.add(perm)
        
        self.stdout.write(self.style.SUCCESS('Successfully set up groups and permissions'))