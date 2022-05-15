from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login, name='login'),
    path('admin-index', views.admin_index, name='admin_index'),
    path('pengguna-index', views.pengguna_index, name='pengguna_index')
]