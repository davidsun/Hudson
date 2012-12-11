# -*- coding: utf8 -*-

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from sns.models import Message
from sns.libs.utils import jsonize, process_login_user


@process_login_user
@jsonize
def user_massage(request, user_id):
    if request.method == 'POST':
        if len(request.POST.get('content', '')) <= 0 or len(request.POST.get('content', '')) > 200:
            return {'status': 'error'}
        user = get_object_or_404(User, pk=user_id)
        m = Message()
        m.sender = request.user
        m.receiver = user
        m.content = request.POST['content']
        m.save()

        CONTENT_LIMIT = 20
        content = m.content
        if len(content) > CONTENT_LIMIT + 3:
            content = content[:CONTENT_LIMIT] + "..."
        user.notifications.create(content=u'@%s 给你留言了：<a href="/messages/">%s</a>'
            % (request.user.username, content))
        return {'status': 'ok'}
    

@process_login_user
def index(request):    
    sent_messages = request.user.sent_messages.order_by('-created_at')
    received_messages = request.user.received_messages.order_by('-created_at')
    followers = list(User.objects.filter(id__in=list(request.user.followers.values_list('follower_id', flat=True)[:5])))
    followees = list(User.objects.filter(id__in=list(request.user.followees.values_list('followee_id', flat=True)[:5])))
    latest_users = list(User.objects.order_by('-date_joined')[:5])
    for follower in followers:
        follower.followed = follower.followers.filter(follower_id=request.user.id).count() > 0
    for followee in followees:
        followee.followed = followee.followers.filter(follower_id=request.user.id).count() > 0
    for latest_user in latest_users:
        latest_user.followed = latest_user.followers.filter(follower_id=request.user.id).count() > 0
    return render_to_response('sns/messages/index', {'followers': followers, 'followees': followees,
        'latest_users': latest_users, 'sent_messages': sent_messages, 'received_messages': received_messages}, context_instance=RequestContext(request))

