from rest_framework import serializers
from .models import ProductType, Product, ProductVariant, LockerType, Locker

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description']

class ProductVariantSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_type = serializers.CharField(source='product.type.name', read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'product_name', 'product_type', 'sku', 'size', 
                  'price', 'deposit', 'weight', 'expiry_date', 'is_active']

class ProductSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type.name', read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'type', 'type_name', 'organization', 
                  'description', 'hazardous', 'variants']
        
class LockerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LockerType
        fields = ['id', 'size', 'description']

class LockerSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    type_size = serializers.CharField(source='type.size', read_only=True)
    
    class Meta:
        model = Locker
        fields = ['id', 'identifier', 'type', 'type_size', 'machine', 
                  'product_variant', 'product_name', 'product_price', 
                  'easy_access', 'state']
    
    def get_product_name(self, obj):
        if obj.product_variant:
            variant = obj.product_variant
            size = f" - {variant.size}" if variant.size else ""
            return f"{variant.product.name}{size}"
        return None
    
    def get_product_price(self, obj):
        if obj.product_variant:
            return obj.product_variant.price
        return None

class InventoryItemSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    product_type = serializers.CharField()
    size = serializers.CharField(allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    available = serializers.IntegerField()

class ComprehensiveMachineSerializer(serializers.Serializer):
    #Machine data
    id = serializers.IntegerField()
    name = serializers.CharField()
    serial_number = serializers.CharField()
    area_code = serializers.CharField()
    
    #Location data
    location_id = serializers.IntegerField()
    location_name = serializers.CharField()
    location_address = serializers.CharField()
    
    #Organization data
    organization_id = serializers.IntegerField()
    organization_name = serializers.CharField()
    
    #Inventory data
    inventory = InventoryItemSerializer(many=True)