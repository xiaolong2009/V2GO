# coding: utf-8
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import Http404
from forum.models import ForumUser, Topic, Favorite, Vote, Reply, Node, Notification, Plane
from django.template import RequestContext

def get_index(request):
	user = request.user
	try:
		current_page = int(request.GET.get('p','1'))
	except ValueError:
		current_page = 1
	if user.is_authenticated():
		counter = {
			'topics': user.topic_author.all().count(),
			'replies': user.reply_author.all().count(),
			'favorites': user.fav_user.all().count(),
		}
		notifications_count = user.notify_user.filter(status=0).count()
	status_counter = {
			'user': ForumUser.objects.all().count(),
			'nodes': Node.objects.all().count(),
			'topics': Topic.objects.all().count(),
			'replies': Reply.objects.all().count(),
	}
	topics, topic_page = Topic.objects.get_all_topic(current_page=current_page)
	planes = Plane.objects.all()
	#planes = Plane.objects.all().prefetch_related('node_set')
	hot_nodes = Node.objects.get_all_hot_nodes()
	active_page = 'topic'
	return render_to_response('topic/topics.html', locals(), context_instance=RequestContext(request))

def get_profile(request, uid):
	try:
		if uid.isdigit():
			user_info = ForumUser.objects.get(pk=uid)
		else:
			user_info = ForumUser.objects.get(username=uid)
	except ForumUser.DoesNotExist:
		raise Http404

	try:
		current_page = int(request.GET.get('p','1'))
	except ValueError:
		current_page = 1

	counter = {
		'topics': Topic.objects.filter(author=user_info).all().count(),
		'replies': Reply.objects.filter(author=user_info).all().count(),
		'favorites': Favorite.objects.filter(owner_user=user_info).all().count()
	}
	user = request.user
	if user.is_authenticated():
		notifications_count = user.notify_user.filter(status=0).count()

	topics, topic_page = Topic.objects.get_user_all_topics(user_info.id, current_page=current_page)
	replies, replie_page = Reply.objects.get_user_all_replies(user_info.id, current_page=current_page)
	return render_to_response('topic/profile.html', locals(),
		context_instance=RequestContext(request))

def get_view(request, topic_id):
	try:
		topic = Topic.objects.get(pk=topic_id)
	except Topic.DoesNotExist:
		raise Http404
	user = request.user
	if user.is_authenticated:
		counter = {
			'topics' : user.topic_author.all().count(),
			'replies': user.reply_author.all().count(),
			'favorites': user.fav_user.all().count()
		}
		notifications_count = user.notify_user.filter(status=0).count()
		topic_favorited = Favorite.objects.filter(involved_topic=topic, owner_user=user).exists()

	reply_num = 106
	reply_count = topic.reply_count
	reply_last_page = (reply_count // reply_num + (reply_count % reply_num and 1)) or 1
	try:
		current_page = int(request.GET.get('p', reply_last_page))
	except ValueError:
		current_page = reply_last_page
	replies, reply_page = Reply.objects.get_all_replies_by_topic_id(topic_id=topic_id, current_page=current_page, num=reply_num)
	active_page = 'topic'
	floor = reply_num * (current_page - 1)

	topic.reply_count = reply_page.total
	topic.hits = (topic.hits or 0) + 1
	topic.save()

	render_to_response('topic.view.html',locals(),
		context_instance=RequestContext(request))


