# views.py
from rest_framework import viewsets
from .models import VippsCredentials, Coupon
from .serializers import VippsCredentialsSerializer, CouponSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

class VippsCredentialsViewSet(viewsets.ModelViewSet):
    queryset = VippsCredentials.objects.all()
    serializer_class = VippsCredentialsSerializer
    permission_classes = [IsAuthenticated] # Restrict access to authenticated users.
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['organization__name', 'merchant_serial_number']
    ordering_fields = ['organization__name', 'environment']


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer