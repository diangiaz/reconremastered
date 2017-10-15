from django.conf.urls import url
from . import views
from django.contrib.auth import views as authViews
from .forms import LoginForm

urlpatterns = [
	url(r'^login/$', authViews.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
	url(r'^logout/$', authViews.logout, {'template_name': 'logout.html', 'next_page': views.adminPage}, name='logout'),
	url(r'^user/$', views.userPage, name='userPage'),
	url(r'^admin/$', views.adminPage, name='adminPage'),
	# url(r'^admin/edituser$', views.editUser, name='edituser'),
	url(r'^admin/createuser$', views.createUser, name='createuser'),
	url(r'^admin/creategroup$', views.createGroup, name='createuser'),
	url(r'^editModal/$', views.editModal, name='editModal'),
	url(r'^editGrp/$', views.editGrp, name='editGrp'),
	url(r'^$', views.adminPage, name='defaultPage'),
]	