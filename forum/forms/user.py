# coding: utf-8
from django import forms
from django.contrib.auth import authenticate
from forum.models import ForumUser
from django.conf import settings

error_messages = {
	'username':{
		'required': u'必须填写用户名',
		'min_length': u'用户名长度过短 （3-12字符）',
		'max_length': u'用户名长度过长（3-12个字符）',
		'invalid': u'用户名格式错误（英文字母开头，数字，下划线构成）'
	},
	'email':{
		'required': u'必须填写E-mail',
		'min_required': u'Email长度有误',
		'max_length': u'Email长度有误',
		'invalid': u'Emial地址无效'
	},
	'password':{
		'required': u'必须填写密码',
		'min_length': u'密码长度过短（6-64个字符）',
		'max_length': u'密码长度过长（6-64个字符）'
	},
}

class LoginForm(forms.Form):
	email = forms.EmailField(min_length=4, max_length=64, 
		error_messages=error_messages.get('email'))
	password = forms.CharField(min_length=6, max_length=64,
		error_messages=error_messages.get('password'))

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)

	def clean(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		if email and password:
			self.user_cache = authenticate(email=email, password=password)
			if self.user_cache is None:
				raise forms.ValidationError(u'邮箱或者密码不正确')
			elif not self.user_cache.is_active:
				raise forms.ValidationError(u"用户已被锁定， 请联系管理员解锁")
		return self.cleaned_data

	def get_user(self):
		return self.user_cache

class RegisterForm(forms.Form):
	username = forms.RegexField(min_length=3, max_length=12, 
		regex=r'^[a-zA-Z][a-zA-Z0-9_]*$',
		error_messages=error_messages.get('username'))
	email = forms.EmailField(min_length=4, max_length=64,
		error_messages=error_messages.get('email'))
	password = forms.CharField(min_length=6, max_length=64,
		error_messages=error_messages.get('password'))
	password_confirm = forms.CharField(required=False)

	#class Meta:
	#	model = ForumUser
	#	field = ('username', )

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		try:
			ForumUser.objects.get(username=username)
			raise forms.ValidationError(u'所填的用户名已经被注册过')
		except ForumUser.DoesNotExist:
			if username in settings.RESERVED:
				raise forms.ValidationError(u'用户名已保留不可用')
			return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		try:
			ForumUser.objects.get(email=email)
			raise forms.ValidationError(u'所填的邮箱已经被注册过')
		except ForumUser.DoesNotExist:
			return email

	def clean_password_confirm(self):
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password_confirm')
		if password1 and password2 and password2 != password1:
			raise forms.ValidationError(u'两次输入密码不一致')
		return password2