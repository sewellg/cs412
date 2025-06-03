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

