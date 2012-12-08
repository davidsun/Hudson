#-*- coding:utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.template import RequestContext
from django.db.models import Count
from sns.models import Post, PostLike, PostTag
from sns.libs.utils import jsonize, notify_at_users, posts_loader, process_login_user, filter_at_users, generate_additional_content
import re


VIDEO_PARAMS = {
    'youku': ('http://player.youku.com/player.php/sid/', lambda elements: [element[3:] for element in elements if element.startswith('id_')][0], '/v.swf'),
    'tudou': ('http://http://www.tudou.com/a/', lambda elements: '', '/v.swf')
}


def get_video_link_type(elements):
    for element in elements:
        if element in VIDEO_PARAMS:
            return element


def get_normalized_video_link(raw_video_link):
    if len(raw_video_link) == 0:
        return '', 0
    elements = re.split(r'\W+', raw_video_link)
    video_type = get_video_link_type(elements)
    if not video_type in VIDEO_PARAMS:
        return '', -1
    video_link = VIDEO_PARAMS[video_type][0] + VIDEO_PARAMS[video_type][1](elements) + VIDEO_PARAMS[video_type][2]
    return video_link, 0


@process_login_user
@jsonize
def index(request):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        image_link = request.POST.get('image_link', '')
        video_link, status = get_normalized_video_link(request.POST.get('video_link', ''))
        if status != 0:
            return {'status': 'error'}
        if len(content) <= 0 or len(content) > 200 or len(image_link) > 200 or len(video_link) > 200:
            return {'status': 'error'}
        if len(image_link) > 0 and len(video_link) > 0:
            return {'status': 'error'}
        original_id = None
        if 'original_id' in request.POST:
            if (Post.objects.filter(original_id=original_id).count() == 0):
                return {'status': 'error'}
            original_id = int(request.POST.get('original_id'))
        post = request.user.posts.create(content=content, original_id=original_id, image_link=image_link, video_link=video_link)

        # get users who has been @, and send notification to them
        notify_at_users(content, "post", post.id, request.user)
        return {'status': 'ok'}


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
    if post.tags.filter(user_id=request.user.id).count() > 0:
        post.user_tag = post.tags.filter(user_id=request.user.id)[0].content
    else:
        post.user_tag = None
    post.tags_list = list(post.tags.values('content').annotate(count=Count('content')))
    post.additional_content = generate_additional_content(post)
    comments = list(post.comments.all())
    return render_to_response('sns/posts/show', {'post': post, 'comments': comments}, context_instance=RequestContext(request))


@process_login_user
@jsonize
def comments(request, post_id):
    if request.method == 'POST':
        if len(request.POST.get('content', '')) > 0 and len(request.POST.get('content', '')) <= 200:
            content = request.POST['content']
            post = get_object_or_404(Post, pk=post_id)
            post.comments.create(content=content, user=request.user)

            # get users who has been @, and send notification to them
            notify_at_users(content, "post_comment", post.id, request.user)
            return {'status': 'ok'}
        else:
            return {'status': 'error'}
    else:
        post = Post.objects.get(id=post_id)
        comments = list(post.comments.prefetch_related("user").all())
        for comment in comments:
            comment.content = filter_at_users(comment.content)
        return comments


@process_login_user
@jsonize
def tags(request, post_id):
    if request.method == 'POST':
        content = request.POST['content']
        if content in PostTag.VALID_TAGS:
            post = get_object_or_404(Post, pk=post_id)
            post.tags.filter(user_id=request.user.id).delete()
            post.tags.get_or_create(user_id=request.user.id, content=content)
            return {'status': 'ok'}
        else:
            return {'status': 'error'}
    else:
        post = get_object_or_404(Post, pk=post_id)
        tags = list(post.tags.values('content').annotate(count=Count('content')))
        if post.tags.filter(user_id=request.user.id).count() > 0:
            user_tag = post.tags.filter(user_id=request.user.id)[0].content
        else:
            user_tag = None
        return {"tags": tags, "user_tag": user_tag}

@process_login_user 
@jsonize
def untag(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        post.tags.filter(user_id=request.user.id).delete()
        return {'status': 'ok'}

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
