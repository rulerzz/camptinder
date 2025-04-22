from rest_framework import serializers
from .models import Location, Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        
class LocationSerializerAlt(serializers.ModelSerializer):
    country_name = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'address', 'city', 'state',
            'zip_code', 'country', 'country_name', 'country_code', 
            'latitude', 'longitude', 'is_active', 'area_code'
        ]
    
    def get_country_name(self, obj):
        return obj.country.country_name if obj.country else None
        
    def get_country_code(self, obj):
        return obj.country.country_code if obj.country else None