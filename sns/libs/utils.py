#-*- coding:utf-8 -*-

import re
import json
from functools import wraps

from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect


def jsonize(func):
    @wraps(func)
    def _(*args, **kwargs):
        result = func(*args, **kwargs)
        return HttpResponse(json.dumps(result), mimetype="application/json")
    return _


def get_notification_template(object_type, object_id):
    if object_type == "post":
        url = "/posts/%s/" % str(object_id)
        tmpl = "@%s 在「<a href='" + url + "'>%s</a>」中提到了你"
    # elif object_type == "xxx"
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
        if not user: continue
        tmpl = get_notification_template(object_type, object_id)
        noti = tmpl % (by_user.username, content)
        user.notifications.create(content=noti)

def filter_at_users(content):
    "Add link to '@somebody'"
    def add_link(username):
        username = username.group(0)[1:].strip()
        try:
            user = User.objects.get(username=username)
        except Exception, e:
            return "@" + username + " "
        return u"<a href='/users/%d/'>@%s</a> " % (user.id, username)
    content = RE_AT_USERS.sub(add_link, content + " ")
    return content.strip()
