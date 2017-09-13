from django.conf.urls import urls
from . import views
from django.contrib.auth import views as authViews

urlpatterns = [
	url(r'^login/$', authViews.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^user/$', views.userPage, name='userPage'),
	url(r'^admin/$', views.adminPage, name='adminPage'),
]