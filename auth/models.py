from django.db import models
from blogs.models import Post

# Create your models here.

class UserProfile(models.Model):
    user_posts = models.ForeignKey(Post)
    user = models.ForeignKey(User, unique=True)

    def __unicode__(self):
        return unicode(self.user)