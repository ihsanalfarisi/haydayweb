from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.read, name='transaksi_pembelian_aset'),
    path('buat', views.create, name='buat_pembelian_aset')
]