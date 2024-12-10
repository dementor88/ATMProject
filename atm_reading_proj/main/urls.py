from django.urls import path
from . import views

urlpatterns = [
    path(r'^info/$', views.info, name='info'),
    path(r'^validate/$', views.validate_user, name='validate'),
    path(r'^activity/$', views.activity, name='login'),
]