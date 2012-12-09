# -*- coding: utf8 -*-

from datetime import date, datetime, timedelta

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from sns.models import Post
from sns.libs.utils import process_login_user


@process_login_user
def index(request):
    if not request.user.is_superuser:
        return redirect('/')
    q = request.GET.get('q', '')
    startdate = request.GET.get('startdate', '')
    enddate = request.GET.get('enddate', '')
    if not startdate:
        startdate = (date.today() + timedelta(days=-7)).strftime('%Y-%m-%d')
    if not enddate:
        enddate = date.today().strftime('%Y-%m-%d')
    # convert 00:00 to 24:00
    enddate_time = (datetime.strptime(enddate, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')

    posts = Post.objects.filter(created_at__range=[startdate, enddate_time])
    if q:
        posts = posts.filter(content__icontains=q).order_by("-created_at")
    result = {}
    total = 0
    for post in posts:
        key = post.created_at.strftime('%Y-%m-%d')
        total += 1
        result[key] = result.get(key, 0) + 1
    data = '['
    for k, v in result.iteritems():
        d = k.split('-')
        data += "[Date.UTC(%s, %s, %s), %d]," % (d[0], d[1], d[2], v)
    if len(result) > 0:
        data = data[:-1]
    data += ']'
    return render_to_response('sns/statistics/index', {
        'q': q,
        'startdate': startdate,
        'enddate': enddate,
        'data': data,
        'total': total
    }, context_instance=RequestContext(request))
