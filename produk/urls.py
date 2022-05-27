from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.read, name='produk'),
    path('produk-admin', views.readadmin, name='produk_admin'),
    path('create-produk', views.create_produk, name='create_produk'),
    path('apply-produk', views.apply_create_produk, name='apply_produk'),
    path('update/<str:produk>', views.check_produk, name='update'),
    path('update/validate/<str:produk>', views.update_produk, name='validate_produk_makanan'),
    path('delete/<str:produk>', views.delete_produk, name='delete'),
]