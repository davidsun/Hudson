from django.contrib.auth.models import User 
from django.db import models 

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    nickname = models.CharField(max_length = 30)
    friends = models.ManyToManyField('self', symmetrical=False, related_name='sns_userprofile_friends', blank=True)

    def __unicode__(self):
        return self.nickname

    class Meta : 
        app_label = 'sns'
