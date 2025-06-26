# File: models.py
# Author: Grace Sewell, gsewell@bu.edu, 6/10/25
# Description: models for final project 

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Squishmallow(models.Model):
    '''class for an individual squishmallow object'''

    name = models.TextField()
    species = models.TextField()

    def __str__(self):
        '''returns string representation of object'''
        return f"{self.name} the {self.species}"

    def load_data():
        '''function to load data from a txt file to generate a database of squishmallow objects'''
        import re

        filename = "/Users/gsewe/django/squishmallows.txt"
        with open(filename, 'r', encoding='utf-8') as f:
            # read every line in file
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            match = re.match(r'^(.+?) the (.+)$', line)
            # strip and match them to the format "name" the "species"
            if match:
                name, species = match.groups()
                # create a new squishmallow object with this info and save it
                squishmallow = Squishmallow(
                                            name = name,
                                            species = species
                )
                squishmallow.save()
        print(f'Created {len(Squishmallow.objects.all())} Squishmallows')

        

class Badge(models.Model):
    '''class for a user's badge'''
    badge_name = models.TextField()

    def __str__(self):
        '''returns string representation of badge object'''
        return f"{self.badge_name} Badge"
    
class Profile(models.Model):
    '''class for an individual profile'''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=True)
    profile_pic = models.ImageField(blank=True)
    fav_squish = models.ForeignKey(Squishmallow, on_delete=models.CASCADE)
    badges = models.ManyToManyField(Badge, blank=True)

    def __str__(self):
        '''returns string representation of object'''
        return f"{self.first_name} {self.last_name}"
    
    def get_collection(self):
        '''finds a profile's collection'''
        return self.user.collection
    
    def get_listings(self):
        '''finds all listings for a user'''
        listings = Listing.objects.filter(owner=self)
        return listings
    
    def get_absolute_url(self):
        '''return url to display one instance of model'''
        return reverse('my_profile')
    
    def add_squish(self, squishmallow):
        '''adds a certain squishmallow to user's collection'''
        self.user.collection.squishmallows.add(squishmallow)
    
    def get_photos(self, squish):
        '''obtains all squishphoto objects belonging to the user'''
        qs = SquishPhoto.objects.filter(squish=squish).filter(profile=self)
        return qs

    def check_badges(self):
        '''checking to see if user has any badges'''
        count = self.user.collection.squishmallows.count()
        # adding specific badges based on user's number of squishmallows
        if count >= 5:
            newcomer_badge = Badge.objects.get(badge_name='Newcomer')
            if newcomer_badge not in self.badges.all():
                self.badges.add(newcomer_badge)
        if count >= 15:
            rising_badge = Badge.objects.get(badge_name='Rising Squish')
            if rising_badge not in self.badges.all():
                self.badges.add(rising_badge)
        if count >= 30:
            fiend_badge = Badge.objects.get(badge_name='Squish Fiend')
            if fiend_badge not in self.badges.all():
                self.badges.add(fiend_badge)
        if count >= 50:
            master_badge = Badge.objects.get(badge_name='Master Squish')
            if master_badge not in self.badges.all():
                self.badges.add(master_badge)
        if count >= 100:
            god_badge = Badge.objects.get(badge_name='Squish God')
            if god_badge not in self.badges.all():
                self.badges.add(god_badge)

class Listing(models.Model):
    '''class for a listing of a squishmallow'''
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    squishmallow = models.ForeignKey(Squishmallow, on_delete=models.CASCADE)
    price = models.IntegerField(blank=False)

    def __str__(self):
        '''returns string representation of a listing'''
        return f"{self.owner.first_name} {self.owner.last_name}'s Listing"
    
    def get_absolute_url(self):
        '''return url to display upon creation of listing'''
        return reverse('show_listing', kwargs={'pk':self.pk})
    
    

class Collection(models.Model):
    '''class for a user's collection'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    squishmallows = models.ManyToManyField(Squishmallow, blank=True)

    def __str__(self):
        '''returns string representation of a collection'''
        return f"{self.user.username}'s Collection"
    
class SquishPhoto(models.Model):
    '''class for a user-specific squishmallow photo'''
    squish = models.ForeignKey(Squishmallow, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    photo = models.ImageField()

    def __str__(self):
        '''returns string representation of a squishphoto'''
        return f"{self.profile.first_name}'s {self.squish.name}"
    
    def get_absolute_url(self):
        '''upon successfully adding photo, return to user's collection'''
        return reverse('collection', kwargs={'pk':self.profile.pk})