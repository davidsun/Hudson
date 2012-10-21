import hamlpy
import simplejson

# Currently all views are here
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from mako.template import Template
from sns.models import Post, PostLike

@login_required(login_url='/login/')
def index(request) :
    if request.method == 'POST' :
        if len(request.POST.get('content', '')) > 0 :
            request.user.posts.create(content=request.POST['content'])
            return HttpResponse(simplejson.dumps({'status': 'ok'}), mimetype="application/json")
        else :
            return HttpResponse(simplejson.dumps({'status': 'error'}), mimetype="application/json")

@login_required(login_url='/login/')
def like(request, post_id):
    liked_post = Post.objects.get(id=post_id)
    liked_post.likes.get_or_create(user_id=request.user.id)
    return HttpResponse(simplejson.dumps({'status': 'ok'}), mimetype="application/json")

@login_required(login_url='/login/')
def unlike(request, post_id):
    PostLike.objects.filter(user_id=request.user.id, post_id=post_id).delete()
    return HttpResponse(simplejson.dumps({'status': 'ok'}), mimetype="application/json")

@login_required(login_url='/login/')
def show(request, post_id):
    post = Post.objects.get(id=post_id)
    post.liked = post.likes.filter(user_id=request.user.id).count() > 0
    return render_to_response('sns/posts/show', {'post':post}, context_instance=RequestContext(request))

