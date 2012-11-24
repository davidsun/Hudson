from django.db import models
from django.contrib.auth.models import User
from sns.models.hudson_model import HudsonModel


class Message(HudsonModel):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, related_name='received_messages')
    sender = models.ForeignKey(User, related_name='sent_messages')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'sns'
