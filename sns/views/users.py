import hamlpy

# Currently all views are here
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mako.template import Template

MAX_MESSAGE_COUNT = 20

@login_required(login_url='/login/')
def home_page(request) :
    message_list = [message for friend in request.user.get_profile().friends.all() for message in
                    sorted(friend.message_set.all(), reverse=True, key=lambda x: x.post_time)[:MAX_MESSAGE_COUNT]]
    message_list.sort(reverse=True, key=lambda x: x.post_time)
    return render_to_response("sns/home_page.html", {'message_list':message_list[:MAX_MESSAGE_COUNT]},
                              context_instance=RequestContext(request))

def index(request) :
    return render_to_response("layout/login_signup")

def login_user(request) : # rename here to avoid name conflict.
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        print "here"
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            print "ok"
            if user.is_active:
                print "ok"
                login(request, user)
                return HttpResponseRedirect(reverse('sns.views.users.home_page'))

    else :
        return render_to_response('sns/login.html', context_instance=RequestContext(request))

@login_required(login_url='/login/')
def show(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render_to_response('sns/user_detail.html', {'user': user})

