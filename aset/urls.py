from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.menu_aset, name='menu_aset'),
    path('read', views.read, name='aset'),
    path('lihat-dekorasi', views.read_dekorasi, name='lihat_dekorasi'),
    path('lihat-bibit', views.read_bibit, name='lihat_dekorasi'),
    path('lihat-kandang', views.read_kandang, name='lihat_kandang'),
    path('lihat-hewan', views.read_hewan, name='lihat_hewan'),
    path('lihat-alatproduksi', views.read_alatproduksi, name='lihat_alatproduksi'),
    path('lihat-petak', views.read_petak, name='lihat_petaksawah'),
]