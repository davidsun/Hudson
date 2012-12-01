from django.db import models
from django.contrib.auth.models import User
from sns.models.hudson_model import HudsonModel


class Post(HudsonModel):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    original = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='posts')

    class Meta:
        app_label = 'sns'
