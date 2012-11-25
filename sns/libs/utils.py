#-*- coding:utf-8 -*-

import re
import json
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def jsonize(func):
    @wraps(func)
    def _(*args, **kwargs):
        result = func(*args, **kwargs)
        return HttpResponse(json.dumps(result), mimetype="application/json")
    return _


def posts_loader(template):
    DEFAULT_LIMIT = 20

    def decorator(func):
        @wraps(func)
        def _(*args, **kwargs):
            request = args[0]
            offset = int(request.GET.get('offset', 0))
            result = func(*args, **kwargs)

            if 'posts' in result:
                posts = result['posts']
                if offset > 0:
                    posts = posts.all()[offset:offset + DEFAULT_LIMIT]
                else:
                    posts = posts.all()[:DEFAULT_LIMIT]
                posts = list(posts)
                for post in posts:
                    post.liked = post.likes.filter(user_id=request.user.id).count() > 0
                for post in posts:
                    post.comments_count = post.comments.count()
                result['posts'] = posts

            if offset > 0:
                return render_to_response('sns/posts/_list', result, context_instance=RequestContext(request))
            else:
                return render_to_response(template, result, context_instance=RequestContext(request))
        return _
    return decorator


def process_login_user(func):
    @wraps(func)
    @login_required
    def _(*args, **kwargs):
        request = args[0]
        request.user.new_notifications = list(request.user.notifications.filter(viewed=False))
        return func(*args, **kwargs)
    return _


def get_notification_template(object_type, object_id):
    if object_type == "post":
        url = "/posts/%s/" % str(object_id)
        tmpl = "@%s 在「<a href='" + url + "'>%s</a>」中提到了你"
    elif object_type == "post_comment":
        url = "/posts/%s/" % str(object_id)
        tmpl = "@%s 在回复「<a href='" + url + "'>%s</a>」中提到了你"
    return unicode(tmpl, 'utf-8')


RE_AT_USERS = re.compile(r'@([^\s@]+)\s')


def notify_at_users(content, object_type, object_id, by_user):
    """
    Get users who has been @, and send notification to them
    TODO: A better way is to refactor notification system by
    adding `object_type`, `object_id` to Model and generate
    url and copywriter by a function with type and id.
    """
    usernames = set(RE_AT_USERS.findall(content + " "))
    # TODO: add consts and import it
    NOTIFI_CONTENT_LIMIT = 15
    if len(content) > NOTIFI_CONTENT_LIMIT + 3:
        content = content[:NOTIFI_CONTENT_LIMIT] + '...'
    content = content.replace("@", "&#64;")
    for username in usernames:
        try:
            user = User.objects.get(username=username)
        except:
            continue
        if not user:
            continue
        tmpl = get_notification_template(object_type, object_id)
        noti = tmpl % (by_user.username, content)
        user.notifications.create(content=noti, viewed=False)


def filter_at_users(content):
    "Add link to '@somebody'"
    def add_link(username):
        username = username.group(0)[1:].strip()
        try:
            user = User.objects.get(username=username)
        except Exception:
            return "@" + username + " "
        return u"<a href='/users/%d/'>@%s</a> " % (user.id, username)
    content = RE_AT_USERS.sub(add_link, content + " ")
    return content.strip()
