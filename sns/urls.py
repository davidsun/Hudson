from django.conf.urls import patterns, include, url

urlpatterns = patterns('sns.views',
    url(r'^(?P<user_id>\d+)/$', 'view_user'),
    url(r'^users/$', 'list_users'),
) 
