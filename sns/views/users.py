from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from sns.models import Post, UserFollow
from sns.libs.utils import jsonize, posts_loader, process_login_user
from sns.views.forms.users import Edit


@process_login_user
@jsonize
def follow(request, user_id):
    if request.user.id != int(user_id):
        user = get_object_or_404(User, pk=user_id)
        user.followers.get_or_create(follower_id=request.user.id)
        return {'status': 'ok'}
    else:
        return {'status': 'error'}


@process_login_user
def followees(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    followees = list(User.objects.filter(id__in=list(user.followees.values_list('followee_id', flat=True))))
    for followee in followees:
        followee.followed = followee.followers.filter(follower_id=request.user.id).count() > 0
    return render_to_response('sns/users/_modal_list', {'users': followees}, context_instance=RequestContext(request))


@process_login_user
def followers(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    followers = list(User.objects.filter(id__in=list(user.followers.values_list('follower_id', flat=True))))
    for follower in followers:
        follower.followed = follower.followers.filter(follower_id=request.user.id).count() > 0
    return render_to_response('sns/users/_modal_list', {'users': followers}, context_instance=RequestContext(request))


@process_login_user
@posts_loader('sns/users/index')
def index(request):
    followers = list(User.objects.filter(id__in=list(request.user.followers.values_list('follower_id', flat=True)[:5])))
    followees = list(User.objects.filter(id__in=list(request.user.followees.values_list('followee_id', flat=True)[:5])))
    latest_users = list(User.objects.order_by('-date_joined')[:5])
    for follower in followers:
        follower.followed = follower.followers.filter(follower_id=request.user.id).count() > 0
    for followee in followees:
        followee.followed = followee.followers.filter(follower_id=request.user.id).count() > 0
    for latest_user in latest_users:
        latest_user.followed = latest_user.followers.filter(follower_id=request.user.id).count() > 0
    followed_ids = list(request.user.followees.values_list('followee_id', flat=True))
    followed_ids.append(request.user.id)
    posts = Post.objects.filter(user_id__in=followed_ids).order_by("-created_at")
    return {'followers': followers, 'followees': followees, 'latest_users': latest_users, 'posts': posts}


def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    from forms.users import Login
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect(reverse('sns.views.users.index'))
        else:
            return render_to_response('sns/users/login', {'form': form}, context_instance=RequestContext(request))
    else:
        form = Login()
        return render_to_response('sns/users/login', {'form': form}, context_instance=RequestContext(request))


@process_login_user
def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('/')


@process_login_user
@posts_loader('sns/users/show')
def show(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.followed = user.followers.filter(follower_id=request.user.id).count() > 0
    followers = list(User.objects.filter(id__in=list(user.followers.values_list('follower_id', flat=True)[:5])))
    followees = list(User.objects.filter(id__in=list(user.followees.values_list('followee_id', flat=True)[:5])))
    for follower in followers:
        follower.followed = follower.followers.filter(follower_id=request.user.id).count() > 0
    for followee in followees:
        followee.followed = followee.followers.filter(follower_id=request.user.id).count() > 0
    posts = Post.objects.filter(user=user).order_by("-created_at")
    return {'followers': followers, 'followees': followees, 'posts': posts, 'user': user}


@process_login_user
def search(request):
    users = list(User.objects.filter(username__icontains=request.GET.get('q', '')).all())
    for user in users:
        user.followed = user.followers.filter(follower_id=request.user.id).count() > 0
    return render_to_response('sns/users/search', {'users': users}, context_instance=RequestContext(request))


def signup(request):
    if request.user.is_authenticated():
        return redirect('/')
    from forms.users import Signup
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render_to_response('sns/users/signup', {'form': form}, context_instance=RequestContext(request))
    else:
        form = Signup()
        return render_to_response('sns/users/signup', {'form': form}, context_instance=RequestContext(request))


@process_login_user
@jsonize
def unfollow(request, user_id):
    UserFollow.objects.filter(follower_id=request.user.id, followee_id=user_id).delete()
    return {'status': 'ok'}


@process_login_user
def edit(request, user_id):
    if int(user_id) != request.user.id:
        return redirect('/')
    if request.method == 'POST':
        form = Edit(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render_to_response('sns/users/edit', {'form': form}, context_instance=RequestContext(request))
    else:
        form = Edit()
        return render_to_response('sns/users/edit', {'form': form}, context_instance=RequestContext(request))


@process_login_user
@jsonize
def contact(request, query):
    # TODO: a better performance sort algorithm ...
    count = int(request.GET.get('count', 5))
    follower_ids = list(request.user.followers.values_list('follower_id', flat=True))
    followee_ids = list(request.user.followees.values_list('followee_id', flat=True))
    contact_ids = list(set(follower_ids + followee_ids))
    contacts = User.objects.filter(id__in=contact_ids)
    prefix = []
    others = []
    other_ids = []
    if query:
        others = []
        contacts = contacts.filter(username__contains=query)
        for u in contacts:
            if u.username.startswith(query):
                prefix.append(u)
            else:
                others.append(u)
                other_ids.append(u.id)
    else:
        others.extend(contacts)
        other_ids.extend(contact_ids)
    chated_ids = list(request.user.sent_messages.all().filter(sender_id__in=other_ids).order_by('-created_at')
        .values_list('receiver_id', flat=True)[:count])
    chated = User.objects.filter(id__in=chated_ids)
    total = []
    total.extend(prefix[:count])
    total.extend(chated[:count])
    total.extend(others[:count])
    result_set = set([])
    result = [u.username for u in total if u.username not in result_set and result_set.add(u.username) is None][:count]
    return {"contacts": result}
