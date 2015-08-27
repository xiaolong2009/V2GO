# coding: utf-8
from django.contrib import auth
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forum.forms.user import RegisterForm, LoginForm
from django.conf import settings
from forum.models import ForumUser

def get_login(request, **kwargs):
	auth.logout(request)
	return render_to_response('user/login.html', kwargs, \
		context_instance=RequestContext(request))

def post_login(request):
	form = LoginForm(request.POST)
	if not form.is_valid():
		return get_login(request, errors=form.errors)
	
	user = form.get_user()
	auth.login(request, user)
	if user.is_staff:
		return redirect(request.REQUEST.get('next', '/manage/admin'))
	return redirect(request.REQUEST.get('next','/'))

def get_register(request, **kwargs):
	auth.logout(request)
	return render_to_response('user/register.html', kwargs,\
		context_instance=RequestContext(request))

def post_register(request):
	form = RegisterForm(request.POST)
	if not form.is_valid():
		return get_register(request, errors=form.errors)
	username = form.cleaned_data['username']
	email = form.cleaned_data['email']
	password = form.cleaned_data['password']
	user = ForumUser.objects.create_user(username=username, email=email, password=password)
	user.save()
	return redirect(settings.LOGIN_URL)

def get_logout(request):
	auth.logout(request)
	return redirect(request.REQUEST.get('next', '/'))

