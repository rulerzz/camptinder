from rest_framework import generics
from .models import Location
from .serializers import LocationSerializer, LocationSerializerAlt
from rest_framework.permissions import AllowAny

class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializerAlt
    permission_classes = [AllowAny]

class LocationDetailView(generics.RetrieveAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializerAlt
    permission_classes = [AllowAny]