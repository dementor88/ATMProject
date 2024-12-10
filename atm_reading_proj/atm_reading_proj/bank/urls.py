from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.get_bank, name='info'),
    path('add/', views.add_bank, name='validate'),
]