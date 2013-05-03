import datetime
from django.db import models
from django.contrib.auth.models import User
#from django.utils import timezone

# Create your models here.

class Poll (models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    total_votes = models.IntegerField(default=0)
    voted = models.BooleanField(default = False)
  
    def __unicode__(self):
        return self.question

    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.admin_order_field = 'pub_date'
    was_published_today.boolean = True
    was_published_today.short_description = 'Published Today?'
 

    #def was_published_recently(self): 
    # return self.pub_date>= timezone.now() - datetime.timedelta(days=1)


class Choice (models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    percentage = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.choice

#class Voter (models.Model):
 #   user = models.ForeignKey(User)
 #   poll = models.ForeignKey(Poll)

 #   def __unicode__(self):
 #       return self.user







