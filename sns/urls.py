from django.conf.urls import patterns, include, url

urlpatterns = patterns('sns.views.users',
    url(r'^/?$', 'index'),
    url(r'^users/(?P<user_id>\d+)/?$', 'show'),
    url(r'^users/(?P<user_id>\d+)/edit/?$', 'edit'),
    url(r'^users/(?P<user_id>\d+)/follow/?$', 'follow'),
    url(r'^users/(?P<user_id>\d+)/unfollow/?$', 'unfollow'),
    url(r'^login/?$', 'login'),
    url(r'^logout/?$', 'logout'),
    url(r'^signup/?$', 'signup'),
    url(r'^users/search/?$', 'search'),
)

urlpatterns += patterns('sns.views.posts',
    url(r'^posts/?$', 'index'),
    url(r'^posts/(?P<post_id>\d+)/like/?$', 'like'),
    url(r'^posts/(?P<post_id>\d+)/unlike/?$', 'unlike'),
    url(r'^posts/(?P<post_id>\d+)/?$', 'show'),
    url(r'^posts/liked/?$', 'liked'),
    url(r'^posts/search/?$', 'search'),
)

urlpatterns += patterns('sns.views.messages',
    url(r'^messages/$', 'post_message'),    
)
