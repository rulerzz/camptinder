from rest_framework import generics, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import  Locker
from machines.models import Machine
from .serializers import (
    ComprehensiveMachineSerializer
)

class PublicMachineDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ComprehensiveMachineSerializer
    
    def retrieve(self, request, *args, **kwargs):
        machine_id = kwargs.get('pk')
        machine = get_object_or_404(Machine, pk=machine_id, is_active=True)
        
        inventory = Locker.objects.filter(
            machine=machine,
            state=Locker.AVAILABLE,
            product_variant__isnull=False
        ).values(
            'product_variant__id',
            'product_variant__product__id',
            'product_variant__product__name', 
            'product_variant__product__type__name',
            'product_variant__size',
            'product_variant__price'
        ).annotate(
            available=Count('id')
        ).order_by('product_variant__product__name', 'product_variant__size')
        
        inventory_data = [
            {
                'variant_id': item['product_variant__id'],
                'product_id': item['product_variant__product__id'],
                'product_name': item['product_variant__product__name'],
                'product_type': item['product_variant__product__type__name'],
                'size': item['product_variant__size'],
                'price': item['product_variant__price'],
                'available': item['available'],
            }
            for item in inventory
        ]
        
        #Response
        response_data = {
            #Machine data
            'id': machine.id,
            'name': machine.name,
            'serial_number': machine.serial_number,
            'area_code': machine.area_code,
            
            #Location data
            'location_id': machine.location.id,
            'location_name': machine.location.name,
            'location_address': f"{machine.location.address}, {machine.location.city}",
            
            #Organization data
            'organization_id': machine.organization.id,
            'organization_name': machine.organization.name,
            
            #Inventory data
            'inventory': inventory_data
        }
        
        serializer = self.get_serializer(response_data)
        return Response(serializer.data)