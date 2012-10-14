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
from sns.models.user_follow import UserFollow

@login_required(login_url='/login/')
def follow(request, user_id) :
    user = User.objects.get(id=user_id)
    user.followers.get_or_create(follower_id=request.user.id)
    return HttpResponse(simplejson.dumps({'status': 'ok'}), mimetype="application/json")

@login_required(login_url='/login/')
def home(request) :
    followers = request.user.followers.all()[:5]
    followees = request.user.followees.all()[:5]
    return render_to_response('sns/users/home', {'followers':followers, 'followees':followees}, context_instance=RequestContext(request))

def login(request) :
    if request.user.is_authenticated() : return redirect('/')
    from forms.users import Login
    if request.method == 'POST' :
        form = Login(request.POST)
        if form.is_valid() :
            form.save(request)
            return HttpResponseRedirect(reverse('sns.views.users.home'))
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
    return render_to_response('sns/user_detail.html', {'user': user})

@login_required(login_url='/login/')
def search(request) :
    users = User.objects.filter(username__icontains=request.GET.get('q', '')).all()
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
def unfollow(request, user_id) :
    UserFollow.objects.filter(follower_id=request.user.id, followee_id=user_id).delete()
    return HttpResponse(simplejson.dumps({'status': 'ok'}), mimetype="application/json")
