from sns.models import Post, UserProfile, Notification
from django.contrib.auth.models import User
from django.contrib import admin

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Notification)

