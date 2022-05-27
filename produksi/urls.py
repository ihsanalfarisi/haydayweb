from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.read, name='produksi'),
    path('produksi-admin', views.readadmin, name='produksi_admin'),
    path('delete/<str:produksi>', views.delete_produksi, name='delete'),
]