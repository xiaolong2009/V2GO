# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url
import xadmin
xadmin.autodiscover()
#from xadmin.plugins import xversion
#xversion.registe_models()
#from django.contrib import admin
#admin.autodiscover()
#xadmin.site.login = login_required(xadmin.site.login)
import forum.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_forum.views.home', name='home'),
    # url(r'^my_forum/', include('my_forum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(forum.urls)), 
    url(r'^manage/admin/', include(xadmin.site.urls)),
)
