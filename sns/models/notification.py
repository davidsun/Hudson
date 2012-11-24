# -*- coding: utf8 -*-

from django.contrib.auth.models import User
from django.db import models
from sns.models import HudsonModel


class Notification(HudsonModel):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='notifications')
    viewed = models.BooleanField(default=False)

    class Meta:
        app_label = 'sns'
