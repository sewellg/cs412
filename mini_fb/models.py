# File: models.py
# Author: Grace Sewell, gsewell@bu.edu, 5/27/25
# Description: models for mini_fb app

from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''encapsulate data of a facebook profile'''
    first_name = models.CharField()
    last_name = models.CharField()
    city = models.CharField(blank=True)
    email_address = models.EmailField()
    profile_image_url = models.URLField()

    def get_status_messages(self):
        statuses = StatusMessage.objects.filter(profile=self)
        return statuses
    
    def get_absolute_url(self):
        '''return url to display one instance of model'''
        return reverse('show_profile', kwargs={'pk':self.pk})


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