from django.conf.urls import url
from . import views
from django.contrib.auth import views as authViews
from .forms import LoginForm

urlpatterns = [
	url(r'^login/$', authViews.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^logout/$', authViews.logout, {'template_name': 'logout.html', 'next_page': views.adminPage}, name='logout'),
	url(r'^user/$', views.userPage, name='userPage'),
	url(r'^admin/$', views.adminPage, name='adminPage'),
	url(r'^getouts$', views.getSerialOutput, name='serialout'),
	url(r'^createUser$', views.createUser, name='createuser'),
	url(r'^createGroup$', views.createGroup, name='creategroup'),
	url(r'^user/reserveDevice$', views.reserveDevice, name='reserveDevice'),
	url(r'^inputSend$', views.inputSend, name='inputSend'),
	url(r'^connectDevices$', views.connectDevices, name='connectDevices'),
	url(r'^disconnectDevices$', views.disconnectDevices, name='connectDevices'),
	url(r'^loadTopology$', views.loadTopology, name='loadTopology'),
	url(r'^saveTopology$', views.saveTopologyFunc, name='saveTopology'),
	url(r'^saveDevice$', views.saveDevice, name='saveDevice'),
	url(r'^saveConnection$', views.saveConnection, name='saveConnection'),
	url(r'^admin/allocateDevice$', views.allocateDevice, name='allocateDevice'),
	url(r'^editModal/$', views.editModal, name='editModal'),
	url(r'^editGrp/$', views.editGrp, name='editGrp'),
	url(r'^user/reserveDevice$', views.reserveDevice, name='reserveDevice'),
	url(r'^approvedRes/$', views.approvedRes, name='approvedRes'),
	url(r'^declinedRes/$', views.declinedRes, name='declinedRes'),
	url(r'^deleteRes/$', views.deleteRes, name='deleteRes'),
	# url(r'^admin/edituser$', views.editUser, name='edituser'),
	url(r'^$', views.adminPage, name='defaultPage'),
]	