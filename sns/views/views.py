# Currently all views are here
from django.shortcuts import render_to_response, get_object_or_404
from sns.models import User

def view_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render_to_response('sns/user_detail.html', {'user': user})

def list_users(request):
    user_list = User.objects.all()[:10]
    print user_list
    return render_to_response("sns/user_list.html", {'user_list': user_list})
