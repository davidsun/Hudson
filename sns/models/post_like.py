# -*- coding: utf8 -*-

from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from sns.models.hudson_model import HudsonModel
from sns.models.post import Post


class PostLike(HudsonModel):
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='likes')
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='post_likes')

    class Meta:
        app_label = 'sns'

    def clean(self):
        objs = PostLike.objects.filter(user_id=self.user_id, post_id=self.post_id).all()
        if len(objs) > 0 and objs[0].id != self.id:
            raise validators.ValidationError(u'不能重复收藏。')
