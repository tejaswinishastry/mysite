import re
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import datetime
from polls.models import Poll
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User)
    poll = models.ForeignKey(Poll)
    categories = models.ManyToManyField(Category)
    title = models.CharField(max_length=500, unique= True)
    slug = models.SlugField(max_length=200, unique= True,
                            unique_for_month= 'date_created') #storing the last part of URL so that every post maps to a unique URL
    date_created = models.DateField()
    tags = models.CharField(max_length=200)
    body = models.TextField()
    body_html = models.TextField(editable=False, blank=True)
    lc_count = models.IntegerField(default=0, editable=False)
    
    def get_tag_list(self):
        return re.split("", self.tags) #return the tags for a post as a list
        #if you have tags seperated by a space it is considered as a seperate tag 

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-date_created"]








