from django.contrib import admin
from django.urls import path, include
from restaurant import views

urlpatterns = [
    path(r'', views.main, name="restaurant"),
    path(r'main/', views.restaurant_main, name="restaurant_main"),
    path(r'order/', views.order, name="order"),
    path(r'confirmation/', views.confirmation, name="confirmation"),
]