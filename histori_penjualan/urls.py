from django import views
from django.contrib import admin
from django.urls import path, include
from . import views
# from .views import detail_pesanan

urlpatterns = [
    path('', views.read, name='histori_penjualan'),
    path('histori_penjualan/detail_pesanan', views.detail_pesanan, name='detail_pesanan')
]