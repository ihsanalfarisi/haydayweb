from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.read, name='histori_produksi_makanan'),
    path('admin', views.readadmin, name='histori_produksi_makanan_admin'),
    path('create-makanan', views.create_makanan, name='create_makanan'),
    path('apply-makanan', views.apply_create_makanan, name='apply_makanan'),
]