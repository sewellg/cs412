# File: forms.py
# Author: Grace Sewell, gsewell@bu.edu, 5/27/25
# Description: forms for mini_fb app

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''a form to add a profile to mini_fb'''
    class Meta():
        '''associate this form with a model from mini_fb'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email_address', 'profile_image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''a form to add a status message'''
    class Meta():
        model = StatusMessage
        fields = ['message']
        
class UpdateProfileForm(forms.ModelForm):
    '''a form to update profiles in mini_fb'''
    class Meta():
        model = Profile
        fields = ['city', 'email_address', 'profile_image_url']

class UpdateStatusForm(forms.ModelForm):
    '''a form to update profiles in mini_fb'''
    class Meta():
        model = StatusMessage
        fields = ['message']