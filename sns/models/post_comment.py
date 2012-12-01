# -*- coding: utf8 -*-

from django.contrib.auth.models import User
from django.db import models
from sns.models.hudson_model import HudsonModel
from sns.models.post import Post


class PostComment(HudsonModel):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comments')
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='post_comments')

    class Meta:
        app_label = 'sns'
