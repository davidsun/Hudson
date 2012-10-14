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

@login_required(login_url='/login/')
def index(request) :
    if request.method == 'POST' :
        if len(request.POST.get('content', '')) > 0 :
            request.user.post_set.create(content=request.POST['content'])
            return HttpResponse(simplejson.dumps({'status': 'ok'}), mimetype="application/json")
        else :
            return HttpResponse(simplejson.dumps({'status': 'error'}), mimetype="application/json")

