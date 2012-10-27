import json
from functools import wraps

from django.http import HttpResponse, HttpResponseRedirect

def jsonize(func):
    @wraps(func)
    def _(*args, **kwargs):
        result = func(*args, **kwargs)
        return HttpResponse(json.dumps(result), mimetype="application/json")
    return _

