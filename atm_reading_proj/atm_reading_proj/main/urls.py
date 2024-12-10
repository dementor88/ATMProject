from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.info, name='info'),
    path('validate/', views.validate, name='validate'),
    path('activity/', views.activity, name='login'),
]