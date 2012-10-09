# Currently all views are here
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from sns.models import Message, UserProfile

MAX_MESSAGE_COUNT = 20
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

def home_page(request):
    message_list = [message for friend in request.user.get_profile().friends.all() for message in friend.message_set.all()[:MAX_MESSAGE_COUNT]]
    print message_list
    message_list.sort(reverse=True, key=lambda x: x.post_time)
    print message_list
    return render_to_response("sns/home_page.html", {'message_list':message_list[:MAX_MESSAGE_COUNT]}, context_instance=RequestContext(request))

def post_message(request):
    m = Message()
    m.user = request.user.get_profile()
    m.content = request.POST['content']
    m.save()
    return HttpResponseRedirect(reverse('sns.views.home_page'))
