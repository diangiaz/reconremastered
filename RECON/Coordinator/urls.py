from django.conf.urls import url
from . import views
from django.contrib.auth import views as authViews
from .forms import LoginForm

urlpatterns = [
	url(r'^login/$', authViews.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^logout/$', authViews.logout, {'template_name': 'logout.html', 'next_page': views.adminPage}, name='logout'),
	url(r'^user/$', views.userPage, name='userPage'),
	url(r'^admin/$', views.adminPage, name='adminPage'),
	url(r'^$', views.adminPage, name='defaultPage'),
	url(r'^getouts1$', views.getSerialOutput1, name='serialout1'),
	url(r'^createUser$', views.createUser, name='createuser'),
	url(r'^createGroup$', views.createGroup, name='creategroup'),
	url(r'^routerSend$', views.sendSerial1, name='sendserial1'),
	url(r'^loadTopology$', views.loadTopology, name='loadTopology'),
	url(r'^saveTopology$', views.saveTopologyFunc, name='saveTopology'),
	url(r'^saveDevice$', views.saveDevice, name='saveDevice'),
	url(r'^saveConnection$', views.saveConnection, name='saveConnection'),
]	