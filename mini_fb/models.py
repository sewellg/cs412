from django.db import models

# Create your models here.

class Profile(models.Model):
    '''encapsulate data of a facebook profile'''
    first_name = models.CharField()
    last_name = models.CharField()
    city = models.CharField(blank=True)
    email_address = models.EmailField()
    profile_image_url = models.URLField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'