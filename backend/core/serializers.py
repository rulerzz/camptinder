from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserRole

User = get_user_model()

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['role_id', 'role_name', 'description']
        read_only_fields = ['role_id']


class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'imageUrl', 'phone', 'role', 'role_name', 'is_active', 'is_verified', 'date_joined']
        read_only_fields = ['id', 'is_active', 'is_verified', 'date_joined']
    
    def get_role_name(self, obj):
        if obj.role:
            return obj.role.get_role_name_display()
        return None


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'imageUrl', 'password', 'password_confirm', 'role']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        #custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        if user.role:
            token['role'] = user.role.role_name
        
        return token
        
    def validate(self, attrs):
        data = super().validate(attrs)
        
        #extra response data
        user = self.user
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'imageUrl': user.imageUrl,
            'is_verified': user.is_verified
        }
        
        if user.role:
            data['user']['role'] = user.role.role_name
            data['user']['role_display'] = user.role.get_role_name_display()
        
        return data