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
from sns.models import Message, UserProfile

@login_required(login_url='/login/')
def post_message(request):
	if request.method == 'POST' :
		if len(request.POST.get('content', '')) > 0 and len(request.POST.get('content',''))<=200 :
			return HttpResponse(simplejson.dumps({'status': 'ok'}), mimetype="application/json")
		else :
			return HttpResponse(simplejson.dumps({'status': 'error'}), mimetype="application/json")

	
	
#@login_required(login_url='/login/')
#def post_message(request):
#	m = Message()
#	m.user = request.user.get_profile()
#	m.content = request.POST['content']
#	m.save()
#	return HttpResponseRedirect(reverse('sns.views.users.home_page'))
 
