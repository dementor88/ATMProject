from django.urls import path
from . import views

urlpatterns = [
    path('get/<int:bank_code>/', views.get_bank, name='get_bank'),
    path('add/', views.add_bank, name='add_bank'),
]