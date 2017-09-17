from django.conf.urls import url
from . import views
from django.contrib.auth import views as authViews
from .forms import LoginForm

urlpatterns = [
	url(r'^login/$', authViews.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^logout/$', authViews.logout, {'template_name': 'logout.html', 'next_page': views.defaultPage}, name='logout'),
	url(r'^user/$', views.userPage, name='userPage'),
	url(r'^admin/$', views.adminPage, name='adminPage'),
	url(r'^$', views.defaultPage, name='defaultPage'),
]	