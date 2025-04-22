from django.urls import path
from .views import PublicMachineListView

urlpatterns = [
    path('machines/', PublicMachineListView.as_view(), name='machine-list')
]
