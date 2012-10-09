import haml

# Currently all views are here
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from mako.template import Template

MAX_MESSAGE_COUNT = 20

def home_page(request) :
    message_list = [message for friend in request.user.get_profile().friends.all() for message in friend.message_set.all()[:MAX_MESSAGE_COUNT]]
    print message_list
    message_list.sort(reverse=True, key=lambda x: x.post_time)
    print message_list
    return render_to_response("sns/home_page.html", {'message_list':message_list[:MAX_MESSAGE_COUNT]}, context_instance=RequestContext(request))

def index(request) :
    return render_to_response("layout/login_signup")

def login(request) :
    if request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render_to_response('sns/user_detail.html', {'user': user})
    else :
        return render_to_response('sns/login.html', context_instance=RequestContext(request))

def show(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render_to_response('sns/user_detail.html', {'user': user})

