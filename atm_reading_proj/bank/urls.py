from django.urls import path
from . import views

urlpatterns = [
    path(r'^get/$', views.get_bank, name='info'),
    path(r'^add/$', views.add_bank, name='validate'),
]