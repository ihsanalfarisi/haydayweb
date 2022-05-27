from django import views
from django.contrib import admin
from django.urls import path, include
from . import views
# from .views import detail_pesanan

urlpatterns = [
    path('', views.read, name='pesanan'),
    path('detail-pesanan', views.detailpesanan, name='detail_pesanan'),
    path('create-pesanan', views.createpesanan, name='create_pesanan')
]