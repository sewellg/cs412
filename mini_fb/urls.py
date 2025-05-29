# File: urls.py
# Author: Grace Sewell, gsewell@bu.edu, 5/27/25
# Description: url patterns for all urls in mini_fb
from django.urls import path
from .views import *

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
]