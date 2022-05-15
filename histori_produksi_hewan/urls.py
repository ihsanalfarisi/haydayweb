from django import views
from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.read, name='histori_produksi_hewan'),
    path('create_histori_hewan', views.CreateHistoriHewan, name='CreateHistoriHewan')
]