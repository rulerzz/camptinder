# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VippsCredentialsViewSet, CouponViewSet

router = DefaultRouter()
router.register(r'vipps-credentials', VippsCredentialsViewSet, basename='vipps-credentials')
router.register(r'coupons', CouponViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
