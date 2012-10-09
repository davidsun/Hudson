import haml

# Currently all views are here
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from mako.template import Template

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

