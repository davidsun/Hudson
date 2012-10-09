from django.conf.urls import patterns, include, url

urlpatterns = patterns('sns.views.users',
    url(r'^$', 'home_page'),
    url(r'^(?P<user_id>\d+)/?$', 'show'),
    url(r'^users/?$', 'index'),
    url(r'^login/?$', 'login_user'),
)

urlpatterns += patterns('sns.views.messages',
    url(r'^post_message/$', 'post_message'),    
)
