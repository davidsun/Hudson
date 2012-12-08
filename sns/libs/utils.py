#-*- coding:utf-8 -*-

import re
import types

from decimal import *
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models 
from django.db.models import Count
from django.db.models.fields.related import ForeignKey
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
from functools import wraps
from sns.models import PostTag


def json_encode(data):
    """
    TODO: Move DATA_BINDING to each model.
    """
    DATA_BINDING = {
        "PostComment": ["content", "created_at", "id", "post_id", "updated_at", "user", "user_id"],
        "User": ["id", "username"]
    }

    def _any(data):
        ret = None
        if type(data) is types.ListType:
            ret = _list(data)
        elif type(data) is types.DictType:
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        avail_attributes = []
        if data.__class__.__name__ in DATA_BINDING:
            avail_attributes = DATA_BINDING[data.__class__.__name__]

        for f in data._meta.fields:
            if len(avail_attributes) == 0 or f.attname in avail_attributes:
                ret[f.attname] = _any(getattr(data, f.attname))
            # Hack into Django's structure ...
            if isinstance(f, ForeignKey) and (len(avail_attributes) == 0 or f.name in avail_attributes) and ('_' + f.name + '_cache') in dir(data):
                ret[f.name] = _any(getattr(data, f.name))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k, v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)
    return json.dumps(ret, cls=DateTimeAwareJSONEncoder)


def jsonize(func):
    @wraps(func)
    def _(*args, **kwargs):
        result = func(*args, **kwargs)
        return HttpResponse(json_encode(result), mimetype="application/json")
    return _


def generate_additional_content(post):
    if len(post.video_link) > 0:
        return "<embed src=\"" + post.video_link + "\" quality=\"high\" width=\"480\" height=\"400\" align=\"middle\" allowScriptAccess=\"always\" allowFullScreen=\"true\" mode=\"transparent\" type=\"application/x-shockwave-flash\"></embed>"
    if len(post.image_link) > 0:
        return "<img src=\"" + post.image_link + "\">"
    return ""

def posts_loader(template):
    DEFAULT_LIMIT = 20

    def decorator(func):
        @wraps(func)
        def _(*args, **kwargs):
            request = args[0]
            offset = int(request.GET.get('offset', 0))
            result = func(*args, **kwargs)

            if 'posts' in result:
                posts = result['posts'].prefetch_related()
                if offset > 0:
                    posts = posts.all()[offset:offset + DEFAULT_LIMIT]
                else:
                    posts = posts.all()[:DEFAULT_LIMIT]
                posts = list(posts)
                for post in posts:
                    post.liked = post.likes.filter(user_id=request.user.id).count() > 0
                    post.comments_count = post.comments.count()
                    if post.tags.filter(user_id=request.user.id).count() > 0:
                        post.user_tag = post.tags.filter(user_id=request.user.id)[0].content
                    else:
                        post.user_tag = None
                    post.tags_list = list(post.tags.values('content').annotate(count=Count('content')))
                    post.additional_content = generate_additional_content(post)
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
        if (not user) or (user.id == by_user.id):
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
