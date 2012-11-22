from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

@login_required
def index(request) :
    followers = list(request.user.followers.all()[:5])
    followees = list(request.user.followees.all()[:5])
    latest_users = list(User.objects.order_by('-date_joined')[:5])
    notifications = list(request.user.notifications.order_by("-created_at").all())
    request.user.notifications.filter(viewed=False).update(viewed=True)
    return render_to_response('sns/notifications/index', {'followers':followers, 'followees':followees, 'latest_users':latest_users, 'notifications' : notifications}, context_instance=RequestContext(request))

