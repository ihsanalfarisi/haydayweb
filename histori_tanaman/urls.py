from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.read, name='histori_tanaman'),
    path('histori_tanaman/create', views.create_produksi, name='create'),
    path('histori_tanaman/validation', views.create_validation_produksi_tanaman, name='validate_produksi')
]