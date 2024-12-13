from django.urls import path
from . import views

urlpatterns = [
    path('get/<int:atm_device_id>/', views.get_atm_device, name='info'),
    path('create/', views.create_atm_deivce, name='validate'),
]