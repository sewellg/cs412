# File: urls.py
# Author: Grace Sewell, gsewell@bu.edu, 5/27/25
# Description: url patterns for all urls in mini_fb
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views    ## NEW
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomepageView.as_view(), name='home'),
    path('profile/<int:pk>', ShowProfileView.as_view(), name='profile'),
    path('profile/', ShowProfileView.as_view(), name="my_profile"),
    path('master_list/', MasterListView.as_view(), name='master'),
    path('listings/', ListingsView.as_view(), name='listings'),
    path('collection/<int:pk>/', CollectionView.as_view(), name='collection'),
    path('show_all_profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('create_profile', CreateProfileView.as_view(), name='create_profile'),
    path('add_squish/<int:squish_id>', AddSquishView.as_view(), name="add_squish"),
    path('create_listing', CreateListingView.as_view(), name='create_listing'),
    path('listing/<int:pk>', ShowListingView.as_view(), name='show_listing'),
    path('listing/<int:pk>/buy/', ConfirmPurchaseView.as_view(), name='confirm_purchase'),
    path('create_photo', CreateSquishPhotoView.as_view(), name='add_photo'),
    path('profile/<int:pk>/listings', ShowProfileListingsView.as_view(), name='profile_listings'),
    path('profile/<int:pk>/delete', DeleteProfileView.as_view(), name='delete_profile'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),
    # login and logout
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', CustomLoginView.as_view(), name = 'login'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)