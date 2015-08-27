from django.conf.urls import patterns, include, url
from views import common, user, topic, notification

urlpatterns = patterns('',
	url(r'^$', common.method_splitter, {'GET': topic.get_index}),
	url(r'^login/$', common.method_splitter, {'GET':user.get_login, 'POST':user.post_login}),
	url(r'^register/$', common.method_splitter, {'GET':user.get_register, 'POST':user.post_register}),
	url(r'^logout/', common.method_splitter, {'GET':user.get_logout}),
	url(r'^u/(.*)/$', common.method_splitter, {'GET':topic.get_profile}),
	url(r'^/t/(\d+)/$', common,method_splitter, {'GET': topic.get_view, 'POST':topic.post_view}),

)