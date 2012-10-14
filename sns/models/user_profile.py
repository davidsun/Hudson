from django.contrib.auth.models import User 
from django.db import models 
from sns.models import HudsonModel

class UserProfile(HudsonModel):
    user = models.OneToOneField(User)

    class Meta : 
        app_label = 'sns'

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
