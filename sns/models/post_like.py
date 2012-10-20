# -*- coding: utf8 -*- 

from django.contrib.auth.models import User
from django.core import validators
from django.db import models 
from sns.models import HudsonModel, Post

class PostLike(HudsonModel) :
    created_at = models.DateTimeField(auto_now_add=True)
    liked_post = models.ForeignKey(Post, related_name='likers')
    liker = models.ForeignKey(User, related_name='liked_posts')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta :
        app_label = 'sns'
    
    def clean(self) :
        objs = PostLike.objects.filter(liker_id=self.liker_id, liked_post_id=self.liked_post_id).all()
        if len(objs) > 0 and objs[0].id != self.id : raise validators.ValidationError(u'不能重复收藏。')
