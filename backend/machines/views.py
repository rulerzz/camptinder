from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Machine
from .serializers import PublicMachineSerializer

class PublicMachineListView(generics.ListAPIView):
    """Public endpoint to list active machines with basic info"""
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicMachineSerializer
    
    def get_queryset(self):
        queryset = Machine.objects.filter(is_active=True)
        
        area_code = self.request.query_params.get('area_code')
        if area_code:
            queryset = queryset.filter(area_code=area_code)
            
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__name__icontains=location)
            
        return queryset