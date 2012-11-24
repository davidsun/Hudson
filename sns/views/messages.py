from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from sns.models import Message
from sns.libs.utils import jsonize, process_login_user


@process_login_user
@jsonize
def index(request, user_id):
    if request.method == 'POST':
        if len(request.POST.get('content', '')) <= 0 or len(request.POST.get('content', '')) > 200:
            return {'status': 'error'}
        user = get_object_or_404(User, pk=user_id)
        m = Message()
        m.sender = request.user
        m.receiver = user
        m.content = request.POST['content']
        m.save()
        return {'status': 'ok'}
