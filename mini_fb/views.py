# File: views.py
# Author: Grace Sewell, gsewell@bu.edu, 5/27/25
# Description: shows all of the views associated with mini_fb app

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class ShowAllProfilesView(ListView):
    '''view class to show all profiles'''

    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllProfilesView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllProfilesView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)

class ShowProfilePageView(DetailView):
    '''view class to show an individual profile'''

    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = "profile"

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def get_object(self):
        current_user = Profile.objects.get(user=self.request.user)
        return current_user
    
class CreateProfileView(CreateView):
    '''view to handle creation of new profile ie. display form to user and process form'''

    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''view to handle creation of status messages'''

    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the profile) to the status
        object before saving it to the database.
        '''
        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.profile = profile # set the FK
        # save status message to database
        sm = form.save()
        # read the file from the form:
        files = self.request.FILES.getlist('files')
        for file in files:
            new_img = Image()
            new_img.image_file = file
            new_img.profile = profile
            new_img.save()

            new_si = StatusImage()
            new_si.status_message = sm
            new_si.image = new_img
            new_si.save()
        
        user = self.request.user
        form.instance.user = user
        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
    def get_object(self):
        current_user = Profile.objects.get(user=self.request.user)
        return current_user
    
    def get_success_url(self):
        '''gets url to display upon successfully submitting form'''
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('show_profile', kwargs={'pk':pk})
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model=Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_object(self):
        current_user = Profile.objects.get(user=self.request.user)
        return current_user
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateProfileView: form.cleaned_data={form.cleaned_data}')

        # find the logged in user
        user = self.request.user
        print(f"CreateProfileView user={user} profile.user={user}")

        # attach user to form instance (Article object):
        form.instance.user = user

        return super().form_valid(form)

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'delete_status'

    def get_object(self):
        current_user = Profile.objects.get(user=self.request.user)
        return current_user
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateProfileView: form.cleaned_data={form.cleaned_data}')

        # find the logged in user
        user = self.request.user
        print(f"CreateProfileView user={user} profile.user={user}")

        # attach user to form instance (Article object):
        form.instance.user = user

        return super().form_valid(form)
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model = StatusMessage
    form_class = UpdateStatusForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'update_status'

    def get_object(self):
        current_user = Profile.objects.get(user=self.request.user)
        return current_user
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateProfileView: form.cleaned_data={form.cleaned_data}')

        # find the logged in user
        user = self.request.user
        print(f"CreateProfileView user={user} profile.user={user}")

        # attach user to form instance (Article object):
        form.instance.user = user

        return super().form_valid(form)
    
class AddFriendView(View):

    def get_object(self):
        current_user = Profile.objects.get(user=self.request.user)
        return current_user
    
    def dispatch(self, request, *args, **kwargs):
        profile1 = Profile.objects.get(user=self.request.user)
        profile2 = Profile.objects.get(pk=self.kwargs['other_pk'])
        profile1.add_friend(profile2)
        return redirect(reverse('show_profile', kwargs={'pk': self.kwargs['pk']}))
    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_object(self):
        current_user = Profile.objects.get(user=self.request.user)
        return current_user
    

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"
    
    def get_object(self):
        current_user = Profile.objects.get(user=self.request.user)
        return current_user
    