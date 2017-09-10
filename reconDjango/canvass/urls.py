from django.conf.urls import url
from . import views
from django.contrib.auth import views as authViews
from .forms import LoginForm


urlpatterns = [
	url(r'^login/$', authViews.login, {'template_name': 'LoginRECON.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^$', views.defaultPage, name='defaultPage'),
    url(r'^user', views.userPage, name='UserPage'),
    url(r'^admin', views.adminPage, name='AdminPage'),
]