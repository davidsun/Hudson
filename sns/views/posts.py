#-*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from sns.models import Post, PostLike
from sns.libs.utils import jsonize, notify_at_users, posts_loader, process_login_user


@process_login_user
@jsonize
def index(request):
    if request.method == 'POST':
        if len(request.POST.get('content', '')) > 0:
            content = request.POST['content']
            post = request.user.posts.create(content=content)

            # get users who has been @, and send notification to them
            notify_at_users(content, "post", post.id, request.user)
            return {'status': 'ok'}
        else:
            return {'status': 'error'}


@process_login_user
@jsonize
def like(request, post_id):
    liked_post = Post.objects.get(id=post_id)
    liked_post.likes.get_or_create(user_id=request.user.id)
    return {'status': 'ok'}


@process_login_user
@jsonize
def unlike(request, post_id):
    PostLike.objects.filter(user_id=request.user.id, post_id=post_id).delete()
    return {'status': 'ok'}


@process_login_user
def show(request, post_id):
    post = Post.objects.get(id=post_id)
    post.liked = post.likes.filter(user_id=request.user.id).count() > 0
    comments = list(post.comments.all())
    return render_to_response('sns/posts/show', {'post': post, 'comments': comments}, context_instance=RequestContext(request))


@process_login_user
def comments(request, post_id):
    if request.method == 'POST':
        return comments_post(request, post_id)
    else:
        post = Post.objects.get(id=post_id)
        comments = list(post.comments.all())
        return render_to_response('sns/posts/_comments_list', {'comments': comments}, context_instance=RequestContext(request))


@jsonize
def comments_post(request, post_id):
    if len(request.POST.get('content', '')) > 0 and len(request.POST.get('content', '')) <= 200:
        content = request.POST['content']
        post = Post.objects.get(id=post_id)
        post.comments.create(content=content, user=request.user)

        # get users who has been @, and send notification to them
        notify_at_users(content, "post", post.id, request.user)
        return {'status': 'ok'}
    else:
        return {'status': 'error'}


@process_login_user
@posts_loader('sns/posts/liked')
def liked(request):
    followers = list(User.objects.filter(id__in=list(request.user.followers.values_list('follower_id', flat=True)[:5])))
    followees = list(User.objects.filter(id__in=list(request.user.followees.values_list('followee_id', flat=True)[:5])))
    latest_users = list(User.objects.order_by('-date_joined')[:5])
    for follower in followers:
        follower.followed = follower.followers.filter(follower_id=request.user.id).count() > 0
    for followee in followees:
        followee.followed = followee.followers.filter(follower_id=request.user.id).count() > 0
    for latest_user in latest_users:
        latest_user.followed = latest_user.followers.filter(follower_id=request.user.id).count() > 0
    liked_id = PostLike.objects.filter(user_id=request.user.id).values('post_id')
    posts = Post.objects.filter(id__in=liked_id).order_by("-created_at")
    return {'followers': followers, 'followees': followees, 'latest_users': latest_users, 'posts': posts}


@process_login_user
@posts_loader('sns/posts/search')
def search(request):
    return {'posts': Post.objects.filter(content__icontains=request.GET.get('q', '')).order_by("-created_at")}
