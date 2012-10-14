from django.contrib.auth.models import User 
from django.db import models 

class UserFollow(models.Model) :
    created_at = models.DateTimeField(auto_now_add=True)
    followee = models.ForeignKey(User, related_name='followers')
    follower = models.ForeignKey(User, related_name='followees')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta :
        app_label = 'sns'
