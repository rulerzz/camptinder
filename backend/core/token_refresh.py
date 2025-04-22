from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    
    def validate(self, attrs):
        request = self.context['request']
        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token is None:
            raise InvalidToken('No valid refresh token found in cookie')
        
        attrs['refresh'] = refresh_token
        
        return super().validate(attrs)


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if 'refresh' in response.data:
            refresh_token = response.data.pop('refresh')
            
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,  #false for development over HTTP
                samesite='Strict',
                max_age=24*60*60  #1 day refresh cookie
            )
        
        return response
    
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            response.delete_cookie('refresh_token')
        
        return super().finalize_response(request, response, *args, **kwargs)