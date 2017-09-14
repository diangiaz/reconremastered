from django.shortcuts import render
from django.template import loader, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from . import forms

# Create your views here.

# @login_required(login_url="/login")
def userPage(request):
	return render(request, 'user.html', {'variable':''})

# @login_required(login_url="/login")	
def adminPage(request):
	return render(request, 'admin.html', {'variable':''})
	
def defaultPage(request):
	return render(request, 'login.html', {'variable':''})