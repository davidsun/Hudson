from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 30)
    nickname = models.CharField(max_length = 30)
    
    def __unicode__(self):
        return self.nickname

    class Meta : 
        app_label = 'sns'
