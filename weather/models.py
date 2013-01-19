from django.db import models

import datetime

class City(models.Model):
 geoid = models.IntegerField(primary_key=True)
 name = models.CharField(max_length=200)
 state = models.CharField(max_length=2)
 population = models.IntegerField()
 latitude = models.FloatField()
 longitude = models.FloatField()

 def __unicode__(self):
  return self.name

class Weather(models.Model):
 latitude = models.FloatField()
 longitude = models.FloatField()
 condition = models.CharField(max_length=100)
 minTemp = models.IntegerField()
 maxTemp = models.IntegerField()
 date = models.DateTimeField()
 #add more attributes here for V2

class Zips(models.Model):
 zipcode = models.IntegerField(primary_key=True)
 latitude = models.FloatField()
 longitude = models.FloatField()

class Campground(models.Model):
 # campID = models.AutoField(primary_key=True)
 latitude = models.FloatField()
 longitude = models.FloatField()
 code = models.CharField(max_length=4)
 name = models.CharField(max_length=200)
 TYEP = models.CharField(max_length=10)
 phone = models.CharField(max_length=25)
 dates = models.CharField(max_length=200)
 notes = models.CharField(max_length=200)
 sites = models.IntegerField()
 elevation = models.IntegerField()
 amenities = models.CharField(max_length=200)



#hi jason, jason here. Im at work and found a much better tutorial of sorts
# http://www.djangobook.com/en/1.0/chapter05/   voila, enjoy it little bitch

#jason here again, here is some stuff on queries
#  https://docs.djangoproject.com/en/dev/ref/models/querysets/#id4

#HI LITTLE TUTORIAL ON ONLY VIEWS & TEMPLATES
# http://www.linuxjournal.com/article/9738?page=0,2