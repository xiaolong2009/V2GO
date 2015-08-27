#from django.contrib import admin
import xadmin
from forum.models import ForumUser, Plane, Node, Topic, Reply, Favorite, Notification, Vote


class ForumUserAdmin(object):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'nickname')
    list_filter = ('is_active', 'is_staff', 'date_joined')


class PlaneAdmin(object):
    list_display = ('name', 'created')
    search_fields = ('name',)
    list_filter = ('created',)


class NodeAdmin(object):
    list_display = ('name', 'slug', 'created')
    search_fields = ('name',)
    list_filter = ('created',)


class TopicAdmin(object):
    list_display = ('title', 'created')
    search_fields = ('title', 'content')
    list_filter = ('created',)


class ReplyAdmin(object):
    list_display = ('content', 'created')
    search_fields = ('content',)
    list_filter = ('created',)


#xadmin.site.register(ForumUser, ForumUserAdmin)
xadmin.site.register(Plane, PlaneAdmin)
xadmin.site.register(Node, NodeAdmin)
xadmin.site.register(Topic, TopicAdmin)
xadmin.site.register(Reply, ReplyAdmin)
xadmin.site.register(Favorite)
xadmin.site.register(Notification)
xadmin.site.register(Vote)

