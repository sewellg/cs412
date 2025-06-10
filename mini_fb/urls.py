# File: urls.py
# Author: Grace Sewell, gsewell@bu.edu, 5/27/25
# Description: url patterns for all urls in mini_fb
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views    ## NEW


urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
    path('profile/', ShowProfilePageView.as_view(), name="show_profile"),
    path('create_profile', CreateProfileView.as_view(), name="create_profile"),
    path('profile/create_status', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
    path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),
    path('profile/add_friend/<int:other_pk>', AddFriendView.as_view(), name="add_friend"),
    path('profile/friend_suggestions', ShowFriendSuggestionsView.as_view(), name="show_friend_suggestions"),
    path('profile/news_feed', ShowNewsFeedView.as_view(), name="show_news_feed"),
    # authentication related urls
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'), ## NEW
	path('logout/', auth_views.LogoutView.as_view(next_page='show_all_profiles'), name='logout'), ## NEW
]