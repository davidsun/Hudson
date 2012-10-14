from django.conf.urls import patterns, include, url

urlpatterns = patterns('sns.views.users',
    url(r'^/?$', 'index'),
    url(r'^(?P<user_id>\d+)/?$', 'show'),
    url(r'^users/(?P<user_id>\d+)/follow?$', 'follow'),
    url(r'^users/(?P<user_id>\d+)/unfollow?$', 'unfollow'),
    url(r'^login/?$', 'login'),
    url(r'^logout/?$', 'logout'),
    url(r'^signup/?$', 'signup'),
    url(r'^users/search/?$', 'search'),
)

urlpatterns += patterns('sns.views.posts',
    url(r'^posts/?$', 'index'),
)

urlpatterns += patterns('sns.views.messages',
    url(r'^post_message/$', 'post_message'),    
)
