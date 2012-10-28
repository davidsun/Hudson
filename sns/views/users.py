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

from sns.models import Post, UserFollow
from sns.libs.utils import jsonize
from sns.views.forms.users import Edit

@login_required(login_url='/login/')
@jsonize
def follow(request, user_id) :
    user = User.objects.get(id=user_id)
    user.followers.get_or_create(follower_id=request.user.id)
    return {'status': 'ok'}

@login_required(login_url='/login/')
def index(request) :
    followers = list(request.user.followers.all()[:5])
    followees = list(request.user.followees.all()[:5])
    latest_users = list(User.objects.order_by('-date_joined')[:5])
    followed_ids = list(request.user.followees.values_list('followee_id', flat=True))
    followed_ids.append(request.user.id)
    posts = list(Post.objects.filter(user_id__in=followed_ids).order_by("-created_at").all())
    for post in posts : post.liked = post.likes.filter(user_id=request.user.id).count() > 0
    return render_to_response('sns/users/index', {'followers':followers, 'followees':followees, 'latest_users':latest_users, 'posts':posts}, context_instance=RequestContext(request))

def login(request) :
    if request.user.is_authenticated() : return redirect('/')
    from forms.users import Login
    if request.method == 'POST' :
        form = Login(request.POST)
        if form.is_valid() :
            form.save(request)
            return HttpResponseRedirect(reverse('sns.views.users.index'))
        else :
            return render_to_response('sns/users/login', {'form':form}, context_instance=RequestContext(request))
    else :
        form = Login()
        return render_to_response('sns/users/login', {'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def logout(request) :
    from django.contrib.auth import logout
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def show(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.followed = user.followers.filter(follower_id=request.user.id).count() > 0
    followers = list(user.followers.all()[:5])
    followees = list(user.followees.all()[:5])
    posts = list(Post.objects.filter(user=user).order_by("-created_at").all())
    for post in posts : post.liked = post.likes.filter(user_id=request.user.id).count() > 0
    return render_to_response('sns/users/show', {'followers':followers, 'followees':followees, 'posts':posts, 'user':user}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def search(request) :
    users = list(User.objects.filter(username__icontains=request.GET.get('q', '')).all())
    for user in users : user.followed = user.followers.filter(follower_id=request.user.id).count() > 0
    return render_to_response('sns/users/search', {'users':users}, context_instance=RequestContext(request)) 

def signup(request) :
    if request.user.is_authenticated() : return redirect('/')
    from forms.users import Signup
    if request.method == 'POST' :
        form = Signup(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('/')
        else :
            return render_to_response('sns/users/signup', {'form':form}, context_instance=RequestContext(request))
    else :
        form = Signup()
        return render_to_response('sns/users/signup', {'form':form}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
@jsonize
def unfollow(request, user_id) :
    UserFollow.objects.filter(follower_id=request.user.id, followee_id=user_id).delete()
    return {'status': 'ok'}

@login_required(login_url='/login/')
def edit(request, user_id) :
    if int(user_id) != request.user.id : return redirect('/')
    if request.method == 'POST':
        form = Edit(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('/')
        else:
            return render_to_response('sns/users/edit', {'form':form}, context_instance=RequestContext(request))
    else:
        form = Edit()
        return render_to_response('sns/users/edit', {'form':form}, context_instance=RequestContext(request))
