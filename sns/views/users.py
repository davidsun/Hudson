import hamlpy

# Currently all views are here
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mako.template import Template

MAX_MESSAGE_COUNT = 20

@login_required(login_url='/login/')
def home(request) :
    message_list = [message for friend in request.user.get_profile().friends.all() for message in
                    sorted(friend.message_set.all(), reverse=True, key=lambda x: x.post_time)[:MAX_MESSAGE_COUNT]]
    message_list.sort(reverse=True, key=lambda x: x.post_time)
    return render_to_response("sns/home_page.html", {'message_list':message_list[:MAX_MESSAGE_COUNT]},
                              context_instance=RequestContext(request))

def login(request) :
    if request.user.is_authenticated() : return redirect('/')
    from forms.user import Login
    if request.method == 'POST' :
        form = Login(request.POST)
        if form.is_valid() :
            form.save(request)
            return HttpResponseRedirect(reverse('sns.views.users.home'))
        else :
            return render_to_response('sns/user/login', {'form':form}, context_instance=RequestContext(request))
    else :
        form = Login()
        return render_to_response('sns/user/login', {'form':form}, context_instance=RequestContext(request))

def logout(request) :
    from django.contrib.auth import logout
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def show(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render_to_response('sns/user_detail.html', {'user': user})

def signup(request) :
    if request.user.is_authenticated() : return redirect('/')
    from forms.user import Signup
    if request.method == 'POST' :
        form = Signup(request.POST)
        if form.is_valid() :
            form.save()
            return redirect('/')
        else :
            return render_to_response('sns/user/signup', {'form':form}, context_instance=RequestContext(request))
    else :
        form = Signup()
        return render_to_response('sns/user/signup', {'form':form}, context_instance=RequestContext(request))
