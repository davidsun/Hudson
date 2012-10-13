from django.conf.urls import patterns, include, url

urlpatterns = patterns('sns.views.users',
    url(r'^$', 'home'),
    url(r'^(?P<user_id>\d+)/?$', 'show'),
    url(r'^login/?$', 'login'),
    url(r'^logout/?$', 'logout'),
    url(r'^signup/?$', 'signup'),
    url(r'^users/?$', 'index'),
)

urlpatterns += patterns('sns.views.messages',
    url(r'^post_message/$', 'post_message'),    
)
