from django.conf.urls import patterns, include, url

urlpatterns = patterns('sns.views',
    url(r'^(?P<user_id>\d+)/$', 'view_user'),
    url(r'^users/$', 'list_users'),
    url(r'^login/$', 'entrance'),
    url(r'^login_user/$', 'login_user'),
) 
