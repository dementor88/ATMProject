from django.urls import path
from . import views

urlpatterns = [
    path('get/<int:bank_code>/', views.get_bank, name='info'),
    path('add/', views.add_bank, name='validate'),
]