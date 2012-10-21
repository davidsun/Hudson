from django.db import models
from django.contrib.auth.models import User
from sns.models.hudson_model import HudsonModel

class Message(HudsonModel):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='messages')

    class Meta : 
        app_label = 'sns'
