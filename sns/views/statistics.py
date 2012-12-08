# -*- coding: utf8 -*-

from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from sns.models import Post, PostLike, PostTag
from sns.libs.utils import jsonize, process_login_user


@process_login_user
def index(request):
    q = request.GET.get('q', '')
    date = request.GET.get('q', '')
    start_date, end_date = date.split('~')
    tag = request.GET.get('tag', '')
    Post.objects.filter(content__icontains=request.GET.get('q', '')).order_by("-created_at")
    return render_to_response('sns/statistics/index', context_instance=RequestContext(request))
