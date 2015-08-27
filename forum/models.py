#coding=utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser

class Pages(object):
    '''
    分页查询工具
    '''
    def __init__(self, count, current_page=1, list_rows=40):
        self.total = count
        self._current = current_page
        self.size = list_rows
        self.pages = self.total // self.size + (1 if self.total % self.size else 0)

        if (self.pages == 0) or (self._current < 1) or (self._current > self.pages):
            self.start = 0
            self.end = 0
            self.index = 1
        else:
            self.start = (self._current - 1) * self.size
            self.end = self.size + self.start
            self.index = self._current
        self.prev = self.index - 1 if self.index > 1 else self.index
        self.next = self.index + 1 if self.index < self.pages else self.index

class NormalTextField(models.TextField):
    def db_type(self, connection):
        return 'text'

#Model objects
class NodeManager(models.Manager):
	'''
	Node objects
	'''
	def get_all_hot_nodes(self):
		query = self.get_query_set().filter(topic__reply_count__gt=0).order_by('topic__reply_count')
		query.query.group_by = ['id']
		return query

class FavoriteManager(models.Manager):
	'''
	Favorite objects
	'''
	def get_user_all_favorites(self, uid, num=16, current_page=1):
		count = self.get_query_set().filter(owner_user__id=uid).count()
		page = Pages(count, current_page, num)
		query = self.get_query_set().select_related('involved_topic','involved_topic__node',\
			'involved_topic__author','involved_topic__last_replied_by').\
			filter(owner_user__id=uid).order_by('-id')[page.start:page.end]
		return query, page

class NotificationManager(models.Manager):
	'''
	Notification objects
	'''
	def get_user_all_notifications(self, uid, num=16, current_page=1):
		count = self.get_query_set().filter(involved_user__id=uid).count()
		page = Pages(count, current_page, num)
		query = self.get_query_set().select_related('involved_user', 'involved_topic', 'trigger_user').\
				filter(involved_user__id=uid).order_by('-id')[page.start:page.end]
		return query, page

class TopicManager(models.Manager):
	'''
	Topic objects
	'''
	def get_all_topic(self, num=36, current_page=1):
		count = self.get_query_set().count()
		page = Pages(count, current_page, num)
		query = self.get_query_set().select_related('author', 'node', 'last_replied_by').\
				all().order_by('-last_touched', '-created', '-last_replied_time', '-id')[page.start:page.end]
		return query, page

	def get_all_topics_by_node_slug(self, num=16, current_page=1, node_slug=None):
		count = self.get_query_set().filter(node__slug==node_slug).count()
		page = Pages(count, current_page, num)
		query = self.get_query_set().select_related('author','node', 'last_replied_by').\
				filter(node__slug=node_slug).order_by('-last_touched', '-created', '-last_replied_time', '-id')[page.start:page.end]
		return query, page

	def get_user_all_topics(self, uid, num=36, current_page=1):
		count = self.get_query_set().filter(author__id=uid).count()
		page = Pages(count, current_page, num)
		query = self.get_query_set().select_related('author', 'last_replied_by', 'node').\
				filter(author__id=uid).order_by('-id')[page.start:page.end]
		return query, page

class ReplyManager(models.Manager):
    '''
    Reply objects
    '''
    def get_user_all_replies(self, uid, num=36, current_page=1):
        count = self.get_query_set().filter(author__id=uid).count()
        page = Pages(count, current_page, num)
        query = self.get_query_set().select_related('topic', 'author').\
                filter(author__id=uid).order_by('-id')[page.start:page.end]
        return query, page

    def get_all_replies_by_topic_id(self, topic_id, num=16, current_page=1):
        count = self.get_query_set().filter(topic__id=topic_id).all().count()
        page = Pages(count, current_page, num)
        query = self.get_query_set().select_related('author', 'topic').\
                filter(topic__id=topic_id).order_by('-created')[page.start:page.end]
        return query, page

class ForumUser(AbstractUser):
    nickname = models.CharField(max_length=200, null=True, blank=True)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    signature = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    company = models.CharField(max_length=50, null=True, blank=True)
    role = models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    reputation = models.IntegerField(null=True, blank=True)
    intro = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    douban = models.CharField(max_length=100, null=True, blank=True)

    def __unicode(self):
        return self.username

class Plane(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

class Node(models.Model):
    name = models.CharField(max_length=200, null=True)
    slug = models.CharField(max_length=200, null=True)
    thumb = models.CharField(max_length=200, null=True, blank=True)
    introduction = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    plane = models.ForeignKey(Plane, null=True, blank=True)
    topic_count = models.IntegerField(null=True, blank=True)
    custom_style = NormalTextField(null=True, blank=True)
    limit_reputation = models.IntegerField(null=True, blank=True)

    objects = NodeManager()

    def __unicode__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    content = NormalTextField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    hits = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    node = models.ForeignKey(Node, null=True, blank=True)
    author = models.ForeignKey(ForumUser, related_name='topic_author', null=True, blank=True)
    reply_count = models.IntegerField(null=True, blank=True)
    last_replied_by =  models.ForeignKey(ForumUser, related_name='topic_last', null=True, blank=True)
    last_replied_time = models.DateTimeField(null=True, blank=True)
    up_vote = models.IntegerField(null=True, blank=True)
    down_vote = models.IntegerField(null=True, blank=True)
    last_touched = models.DateTimeField(null=True, blank=True)

    objects = TopicManager()

    def __unicode__(self):
        return self.title

class Reply(models.Model):
    topic = models.ForeignKey(Topic, related_name='reply_topic', null=True, blank=True)
    author = models.ForeignKey(ForumUser,related_name='reply_author', null=True, blank=True)
    content = NormalTextField(max_length=200, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    up_vote = models.IntegerField(null=True, blank=True)
    down_vote = models.IntegerField(null=True, blank=True)
    last_touched = models.DateTimeField(null=True, blank=True)

    objects = ReplyManager()

class Notification(models.Model):
    content = NormalTextField(max_length=200)
    status = models.IntegerField(null=True, blank=True)
    involved_type = models.IntegerField(null=True, blank=True)
    involved_user = models.ForeignKey(ForumUser,related_name='notify_user', null=True, blank=True)
    involved_topic = models.ForeignKey(Topic,related_name='notify_topic', null=True, blank=True)
    involved_reply = models.ForeignKey(Reply,related_name='notify_reply', null=True, blank=True)
    trigger_user = models.ForeignKey(ForumUser,related_name='notify_trigger', null=True, blank=True)
    occurrence_time = models.DateTimeField(null=True, blank=True)

    objects = NotificationManager()
    
class Favorite(models.Model):
    owner_user = models.ForeignKey(ForumUser, related_name='fav_user', null=True, blank=True)
    involved_type = models.IntegerField(null=True, blank=True)
    involved_topic = models.ForeignKey(Topic, related_name='fav_topic', null=True, blank=True)
    involved_reply = models.ForeignKey(Reply, related_name='fav_reply', null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)

    objects = FavoriteManager()

class Transation(models.Model):
    type = models.IntegerField(null=True, blank=True)
    reward = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(ForumUser, related_name='trans_user', null=True, blank=True)
    current_balance = models.IntegerField(null=True, blank=True)
    involved_user = models.ForeignKey(ForumUser, related_name='trans_involved', null=True, blank=True)
    involved_topic = models.ForeignKey(Topic, related_name='trans_topic', null=True, blank=True)
    involved_reply = models.ForeignKey(Reply, related_name='trans_reply', null=True, blank=True)
    occurrence_time = models.DateTimeField(null=True, blank=True)

class Vote(models.Model):
    status = models.IntegerField(null=True, blank=True)
    involved_type = models.IntegerField(null=True, blank=True)
    involved_user = models.ForeignKey(ForumUser, related_name='vote_user', null=True, blank=True)
    involved_topic = models.ForeignKey(Topic, related_name='vote_topic', null=True, blank=True)
    involved_reply = models.ForeignKey(Reply, related_name='vote_reply', null=True, blank=True)
    trigger_user = models.ForeignKey(ForumUser, related_name='vote_trigger', null=True, blank=True)
    occurrence_time = models.DateTimeField(null=True, blank=True)


