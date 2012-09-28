from django.db import models

class User(models.Model) :
    id = models.BigIntegerField(primary_key = True)
    name = models.CharField(max_length = 30)
    nickname = models.CharField(max_length = 30)

    class Meta : 
        app_label = 'sns'
