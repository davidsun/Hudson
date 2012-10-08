# Currently all views are here
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext

def view_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render_to_response('sns/user_detail.html', {'user': user})

def list_users(request):
    user_list = User.objects.all()[:10]
    print user_list
    return render_to_response("sns/user_list.html", {'user_list': user_list})

def entrance(request):
    return render_to_response('sns/login.html', context_instance=RequestContext(request))

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response('sns/user_detail.html', {'user': user})

