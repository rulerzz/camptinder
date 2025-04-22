from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView, 
    CustomTokenObtainPairView,
    UserProfileView,
    LogoutView
)
from .token_refresh import CookieTokenRefreshView

urlpatterns = [
    #auth endpoints
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    #user endpoints
    path('users/profile/', UserProfileView.as_view(), name='user_profile'),
]