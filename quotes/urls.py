from django.urls import path
from django.conf import settings
from quotes import views

urlpatterns = [ 
    path(r'', views.main, name="main"),
    path(r'about/', views.about, name="about"),
    path(r'quote/', views.quote, name="quote"),
    path(r'show_all/', views.show_all, name="show_all")

]