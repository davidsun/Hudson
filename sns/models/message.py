from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User)
    post_time = models.DateTimeField('time posted')
    content = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.content

    class Meta : 
        app_label = 'sns'
