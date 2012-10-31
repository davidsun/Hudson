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

from sns.models import Post, PostLike
from sns.libs.utils import jsonize

@login_required(login_url='/login/')
@jsonize
def index(request) :
    if request.method == 'POST' :
        if len(request.POST.get('content', '')) > 0 :
            request.user.posts.create(content=request.POST['content'])
            return {'status': 'ok'}
        else :
            return {'status': 'error'}

@login_required(login_url='/login/')
@jsonize
def like(request, post_id):
    liked_post = Post.objects.get(id=post_id)
    liked_post.likes.get_or_create(user_id=request.user.id)
    return {'status': 'ok'}

@login_required(login_url='/login/')
def unlike(request, post_id):
    PostLike.objects.filter(user_id=request.user.id, post_id=post_id).delete()
    return {'status': 'ok'}

@login_required(login_url='/login/')
def show(request, post_id):
    post = Post.objects.get(id=post_id)
    post.liked = post.likes.filter(user_id=request.user.id).count() > 0
    return render_to_response('sns/posts/show', {'post':post}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def liked(request):
    liked_id = PostLike.objects.filter(user_id=request.user.id).values('post_id')
    posts = Post.objects.filter(id__in=liked_id)
    return render_to_response('sns/posts/liked', {'posts':posts}, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
def search(request) :
    posts = list(Post.objects.filter(content__icontains=request.GET.get('q', '')).order_by("-created_at").all())
    for post in posts : post.liked = post.likes.filter(user_id=request.user.id).count() > 0
    return render_to_response('sns/posts/search', {'posts':posts}, context_instance=RequestContext(request)) 


