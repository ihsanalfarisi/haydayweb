from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.menu_aset, name='menu_aset'),
    path('read', views.read, name='aset'),
    path('lihat-dekorasi', views.read_dekorasi, name='lihat_dekorasi'),
    path('lihat-bibit', views.read_bibit, name='lihat_bibit'),
    path('lihat-kandang', views.read_kandang, name='lihat_kandang'),
    path('lihat-hewan', views.read_hewan, name='lihat_hewan'),
    path('lihat-alatproduksi', views.read_alatproduksi, name='lihat_alatproduksi'),
    path('lihat-petak', views.read_petak, name='lihat_petaksawah'),

    path('buat', views.menu_buat, name='menu_buat'),
    path('buat-dekorasi', views.buat_dekorasi, name='buat_dekorasi'),
    path('buat-bibit', views.buat_bibit, name='buat_bibit'),
    path('buat-kandang', views.buat_kandang, name='buat_kandang'),
    path('buat-hewan', views.buat_hewan, name='buat_hewan'),
    path('buat-alat', views.buat_alat, name='buat_alat'),
    path('buat-petak', views.buat_petak, name='buat_petak'),

    path('update-dekorasi/<str:id>', views.update_dekorasi, name='update_dekorasi'),
    path('update-bibit/<str:id>', views.update_bibit, name='update_bibit'),
    path('update-kandang/<str:id>', views.update_kandang, name='update_kandang'),
    path('update-hewan/<str:id>', views.update_hewan, name='update_hewan'),
    path('update-alat/<str:id>', views.update_alat, name='update_alat'),
    path('update-petak/<str:id>', views.update_petak, name='update_petak'),

    path('delete-dekorasi/<str:id>', views.delete_dekorasi, name='delete_dekorasi'),
    path('delete-bibit/<str:id>', views.delete_bibit, name='delete_bibit'),
    path('delete-kandang/<str:id>', views.delete_kandang, name='delete_kandang'),
    path('delete-hewan/<str:id>', views.delete_hewan, name='delete_hewan'),
    path('delete-alat/<str:id>', views.delete_alat, name='delete_alat'),
    path('delete-petak/<str:id>', views.delete_petak, name='delete_petak'),
]
