from django.urls import path, include
from .views import (
    PublicMachineDetailView,
)

urlpatterns = [
    path('machines/inventory/<int:pk>/', PublicMachineDetailView.as_view(), name='public-machine-detail'),
]