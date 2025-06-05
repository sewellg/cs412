# File: models.py
# Author: Grace Sewell, gsewell@bu.edu, 5/27/25
# Description: models for mini_fb app

from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''encapsulate data of a facebook profile'''

    # data attributes for a profile
    first_name = models.CharField()
    last_name = models.CharField()
    city = models.CharField(blank=True)
    email_address = models.EmailField()
    profile_image_url = models.URLField()

    def get_status_messages(self):
        '''filters all status messages by their profile'''
        
        statuses = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return statuses
    
    def get_absolute_url(self):
        '''return url to display one instance of model'''
        return reverse('show_profile', kwargs={'pk':self.pk})

    def get_friends(self):
        friends_list = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)
        profile_list = []
        for item in friends_list:
            if item.profile1 != self:
                profile_list.append(item.profile1)
            elif item.profile2 != self:
                profile_list.append(item.profile2)
        return profile_list
    
    def add_friend(self, other):
        ''''''
        if Friend.objects.filter(profile1=self, profile2=other).exists() == False:
            new_instance = Friend(profile1=self, profile2=other)
            new_instance.save()

    def get_friend_suggestions(self):
        all_profiles = Profile.objects.all()
        current_friends = self.get_friends()
        possible_friends = []
        for profile in all_profiles:
            if profile not in current_friends:
                if profile!=self:
                    possible_friends.append(profile)
        print(possible_friends)
        return possible_friends

    def __str__(self):
        # replaces default self with a title of the profile's first and last name
        return f'{self.first_name} {self.last_name}'
    
class StatusMessage(models.Model):
    '''encapsulates data of a profile's status message'''

    # data attributes of status message objects

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.message}"
    
    def get_images(self):
        images = StatusImage.objects.filter(status_message=self)
        
        return images
    
class Image(models.Model):
    '''encapsulates data of an image'''
    # data attributes of images
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField()
    caption = models.CharField(blank=True)

class StatusImage(models.Model):
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.TimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile1.first_name} {self.profile1.last_name} + {self.profile2.first_name} {self.profile2.last_name}'
    
    