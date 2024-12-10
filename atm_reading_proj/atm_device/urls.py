from django.urls import path
from . import views

urlpatterns = [
    path(r'^get/$', views.get_atm_device, name='info'),
    path(r'^create/$', views.create_atm_deivce, name='validate'),
]