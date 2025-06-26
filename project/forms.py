from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):
    '''form to add profile to squish tracker'''
    class Meta():
        # associate this form with a model from project
        model = Profile
        fields = ['first_name', 'last_name', 'profile_pic', 'fav_squish']

class CreateListingForm(forms.ModelForm):
    '''form to add a listing'''
    class Meta():
        model=Listing
        fields = ['squishmallow','price']

    def __init__(self, *args, user=None, **kwargs):
        '''initialize queryset so that user can only list their own squishmallows'''
        super().__init__(*args, **kwargs)
        if user:
            squish_qs = user.collection.squishmallows.all()
            self.fields['squishmallow'].queryset = squish_qs

class CreateSquishPhotoForm(forms.ModelForm):
    '''form to create a squishphoto model instance'''
    class Meta():
        model = SquishPhoto
        fields = ['squish', 'photo']

    def __init__(self, *args, user=None, **kwargs):
        '''initialize so that the user can only add photos for squishmallows they own'''
        super().__init__(*args, **kwargs)
        if user:
            squish_qs = user.collection.squishmallows.all()
            self.fields['squish'].queryset = squish_qs
            # if user is adding a squishphoto from clicking on the squish they own, automatically set the squish field to the one they clicked on
            if 'squish' in self.initial and self.initial['squish'] not in squish_qs:
                self.initial['squish'] = None

class UpdateProfileForm(forms.ModelForm):
    '''form to update a profile'''
    class Meta():
        model = Profile
        fields = ['fav_squish', 'profile_pic']

