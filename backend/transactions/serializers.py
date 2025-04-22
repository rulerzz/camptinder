from rest_framework import serializers
from .models import VippsCredentials, Coupon

class VippsCredentialsSerializer(serializers.ModelSerializer):
    organization_name = serializers.ReadOnlyField(source='organization.name')
    
    class Meta:
        model = VippsCredentials
        fields = ['id', 'organization', 'organization_name', 'environment', 'client_id', 
                 'client_secret', 'subscription_key', 'merchant_serial_number', 'is_active']
        extra_kwargs = {
            'client_id': {'write_only': True},
            'client_secret': {'write_only': True},
            'subscription_key': {'write_only': True},
        }

class CouponSerializer(serializers.ModelSerializer):
    discount_display = serializers.CharField(source='get_discount_display', read_only=True)
    is_valid = serializers.BooleanField(source='is_valid', read_only=True)

    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'organization', 'discount_type', 'discount_value',
            'product_type', 'product', 'valid_from', 'valid_until',
            'max_uses', 'used_count', 'is_active',
            'discount_display', 'is_valid'
        ]