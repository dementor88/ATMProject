from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.get_atm_device, name='info'),
    path('create/', views.create_atm_deivce, name='validate'),
]