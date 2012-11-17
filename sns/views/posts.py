#-*- coding:utf-8 -*-

import hamlpy
import json

# Currently all views are here
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from mako.template import Template

from sns.models import Post, PostLike, PostComment
from sns.libs.utils import jsonize, notify_at_users, posts_loader

@login_required
@jsonize
def index(request) :
    if request.method == 'POST' :
        if len(request.POST.get('content', '')) > 0 :
            content = request.POST['content']
            post = request.user.posts.create(content=content)

            # get users who has been @, and send notification to them
            notify_at_users(content, "post", post.id, request.user)

            return {'status': 'ok'}
        else :
            return {'status': 'error'}

@login_required
@jsonize
def like(request, post_id):
    liked_post = Post.objects.get(id=post_id)
    liked_post.likes.get_or_create(user_id=request.user.id)
    return {'status': 'ok'}

@login_required
@jsonize
def unlike(request, post_id):
    PostLike.objects.filter(user_id=request.user.id, post_id=post_id).delete()
    return {'status': 'ok'}

@login_required
def show(request, post_id):
    post = Post.objects.get(id=post_id)
    post.liked = post.likes.filter(user_id=request.user.id).count() > 0
    comments = list(post.comments.all())
    return render_to_response('sns/posts/show', {'post':post, 'comments':comments}, context_instance=RequestContext(request))

@login_required
@posts_loader('sns/posts/liked')
def liked(request):
    followers = list(request.user.followers.all()[:5])
    followees = list(request.user.followees.all()[:5])
    latest_users = list(User.objects.order_by('-date_joined')[:5])
    liked_id = PostLike.objects.filter(user_id=request.user.id).values('post_id')
    posts = Post.objects.filter(id__in=liked_id).order_by("-created_at")
    return {'followers':followers, 'followees':followees, 'latest_users':latest_users, 'posts':posts}
    
@login_required
@posts_loader('sns/posts/search')
def search(request) :
    return {'posts':Post.objects.filter(content__icontains=request.GET.get('q', '')).order_by("-created_at")}

@login_required
def get_comments(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = list(post.comments.all())
    count = len(comments)
    return render_to_response('sns/posts/_comments_list', {'comments':comments, 'count':count}, context_instance=RequestContext(request))
    
@login_required
@jsonize
def post_comment(request):
    if request.method == 'POST' :
        if len(request.POST.get('content','')) > 0 and len(request.POST.get('content',''))<=200 :
            content = request.POST['content']
            post_id = int(request.POST['post_id'])
            post = Post.objects.get(id=post_id)
            post.comments.create(content=content,user=request.user)

            #get users who has been @, and send notification to them 
            notify_at_users(content, "post", post.id, request.user)
            return {'status': 'ok'}
        else :
            return {'status': 'error'} 


