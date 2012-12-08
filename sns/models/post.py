# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import User
from sns.models.hudson_model import HudsonModel


class Post(HudsonModel):
    VALID_TAGS = [u'顶', u'踩', u'这是谣言']

    content = models.CharField(max_length=200)
    image_link = models.CharField(max_length=200, blank=True)
    video_link = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    original = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='posts')

    class Meta:
        app_label = 'sns'
