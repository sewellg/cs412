# File: models.py
# Author: Grace Sewell, gsewell@bu.edu, 6/10/25
# Description: models for final project 

from django.db import models

# Create your models here.

class Genre(models.Model):
    '''encapsulate data for a genre model'''

    # data attributes for genre model
    genre_name = models.CharField()

class Artist(models.Model):
    '''encapsulate data for an artist model'''

    # data attributes for artist model
    artist_name = models.CharField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

class Song(models.Model):
    '''encapsulate data for a song model'''

    # data attributes for song model
    song_name = models.CharField()
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    
class Profile(models.Model):
    '''encapsulate data for a profile model'''

    # data attributes for profile model
    first_name = models.CharField()
    last_name = models.CharField()
    fav_genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True)
    fav_song = models.ForeignKey(Song, on_delete=models.CASCADE, blank=True)
    fav_artist = models.ForeignKey(Artist, on_delete=models.CASCADE, blank=True)
