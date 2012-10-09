from django.conf.urls import patterns, include, url

urlpatterns = patterns('sns.views.users',
    url(r'^(?P<user_id>\d+)/?$', 'show'),
    url(r'^users/?$', 'index'),
    url(r'^login/?$', 'login'),
) 
