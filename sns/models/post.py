from django.db import models
from django.contrib.auth.models import User
from sns.models import HudsonModel

class Post(HudsonModel):
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta : 
        app_label = 'sns'
