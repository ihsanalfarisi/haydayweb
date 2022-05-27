from django import views
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.read, name='transaksi_upgrade_lumbung'),
    path('upgrade_lumbung', views.create, name='upgrade_lumbung'),
    path('upgrade_lumbung/validation/<str:level>/<str:next_level>/<str:kapasitas>/<str:next_kapasitas>', views.create_validation_upgrade_lumbung, name='validation'),
]