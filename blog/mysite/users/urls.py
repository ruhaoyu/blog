# coding=utf-8
'''for application users define url'''

from django.conf.urls import url
from django.contrib.auth.views import login, password_change, password_change_done


from . import views

urlpatterns = [
	# login
	url(r'^login/$', login,
		{'template_name': 'users/login1.html'},
		name='login'),
	url(r'^logout/$', views.logout_view,
		name='logout'),
	url(r'^register/$', views.register_view,
		name='register'),
	url(r'^password_change/$', password_change, 
		name='password_change'),
	url(r'^password_change_done/$', password_change_done, 
		name='password_change_done'),
]