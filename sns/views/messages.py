# Currently all views are here
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from sns.models import Message, UserProfile

@login_required(login_url='/login/')
def post_message(request):
    m = Message()
    m.user = request.user.get_profile()
    m.content = request.POST['content']
    m.save()
    return HttpResponseRedirect(reverse('sns.views.users.home_page'))
 
