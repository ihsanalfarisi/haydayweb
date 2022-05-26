from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.read, name='histori_tanaman'),
    path('create', views.create_produksi, name='create'),
    path('validation', views.create_validation_produksi_tanaman, name='validate')
]