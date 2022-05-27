from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('paket_koin/read', views.read_paketkoin, name='paket_koin'),
    path('transaksi/read', views.read_transaksi, name='transaksi_pembelian_koin'),
    path('paket_koin/create', views.create_paketkoin, name='create'),
    path('paket_koin/validation', views.create_validation_paketkoin, name='validation'),
    path('transaksi/create/<str:paket_koin>/<str:harga>', views.check_jumlah_transaksi, name='create_beli'),
    path('transaksi/validation/<str:paket_koin>', views.create_validation_transaksi, name='validate'),
    path('paket_koin/update/<str:paket_koin>', views.check_koin, name='updateKoin'),
    path('paket_koin/update/validate/<str:paket_koin>', views.update_koin, name='updatevalidate'),
    path('paket_koin/delete/<str:paket_koin>', views.delete_koin, name='deleteKoin')
]