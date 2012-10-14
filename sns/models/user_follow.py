# -*- coding: utf8 -*- 

from django.contrib.auth.models import User 
from django.core import validators
from django.db import models 
from sns.models import HudsonModel

class UserFollow(HudsonModel) :
    created_at = models.DateTimeField(auto_now_add=True)
    followee = models.ForeignKey(User, related_name='followers')
    follower = models.ForeignKey(User, related_name='followees')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta :
        app_label = 'sns'
    
    def clean(self) :
        if self.followee_id == self.follower_id : raise validators.ValidationError(u'关注者和被关注者不能相同。')
        objs = UserFollow.objects.filter(follower_id=self.follower_id, followee_id=self.followee_id).all()
        if len(objs) > 0 and objs[0].id != self.id : raise validators.ValidationError(u'不能重复关注。')

