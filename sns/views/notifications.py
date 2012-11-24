from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from sns.libs.utils import process_login_user


@process_login_user
def index(request):
    followers = list(User.objects.filter(id__in=list(request.user.followers.values_list('follower_id', flat=True)[:5])))
    followees = list(User.objects.filter(id__in=list(request.user.followees.values_list('followee_id', flat=True)[:5])))
    latest_users = list(User.objects.order_by('-date_joined')[:5])
    for follower in followers:
        follower.followed = follower.followers.filter(follower_id=request.user.id).count() > 0
    for followee in followees:
        followee.followed = followee.followers.filter(follower_id=request.user.id).count() > 0
    for latest_user in latest_users:
        latest_user.followed = latest_user.followers.filter(follower_id=request.user.id).count() > 0
    notifications = list(request.user.notifications.order_by("-created_at").all())
    request.user.notifications.filter(viewed=False).update(viewed=True)
    return render_to_response('sns/notifications/index', {'followers': followers, 'followees': followees,
        'latest_users': latest_users, 'notifications': notifications}, context_instance=RequestContext(request))
