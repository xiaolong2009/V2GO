# coding: utf-8

import re
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.conf import settings

def method_splitter(request, *arg, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *arg, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *arg, **kwargs)
    raise Http404

def send_mail(title, content, to):
    msg = EmailMultiAlternatives(title, content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(content, 'text/html')
    msg.send()