from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.read, name='lumbung'),
    path('lumbung-admin', views.readadmin, name='lumbung_admin'),
]