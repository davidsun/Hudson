from django.db import models
from django.contrib.auth.models import User
from sns.models.user_profile import UserProfile

class Message(models.Model):
    user = models.ForeignKey(UserProfile)
    post_time = models.DateTimeField('time posted', auto_now_add=True)
    content = models.CharField(max_length=200)

    def __unicode__(self):
        return self.content

    class Meta : 
        app_label = 'sns'
