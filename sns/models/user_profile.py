from django.contrib.auth.models import User 
from django.db import models 

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    friends = models.ManyToManyField('self', symmetrical=False, related_name='sns_userprofile_friends', blank=True)

    class Meta : 
        app_label = 'sns'

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
