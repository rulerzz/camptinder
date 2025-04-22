from rest_framework import serializers
from .models import Machine

class PublicMachineSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = Machine
        fields = ['id', 'name', 'serial_number', 'location_name', 'area_code']