from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from . import forms
from .forms import SignUpForm, CreateGroupForm#, UserGroupForm
from .models import Group, Profile

import json
import urllib.parse as urlparse
# Create your views here.




		
@login_required(login_url="/login")
def userPage(request):
	currentUser = request.user
	
	if currentUser.profile.usertype == 'admin':
		return HttpResponseRedirect("/admin/")

	users = User.objects.all()	
	context = {
		'current_user': currentUser
	}
	return render(request, 'user.html', context)

@login_required(login_url="/login")	
def adminPage(request):
	currentUser = request.user
	
	if currentUser.profile.usertype == 'employee':
		return HttpResponseRedirect("/user/")
	
	signupForm = SignUpForm()
	newgroupForm = CreateGroupForm()
	users = User.objects.all()	
	
	
	context = {
	'users':users,
	'current_user': currentUser,
	'newgroupForm': newgroupForm,
	'signupForm' : signupForm,
	}
	return render(request, 'admin.html', context)
	
@login_required(login_url="/login")	
def createUser(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid() and User.objects.all().filter(username__iexact=form.cleaned_data.get('username')).count() == 0 and User.objects.all().filter(email__iexact=form.cleaned_data.get('email')).count() == 0 and Profile.objects.all().filter(employeeID__iexact=form.cleaned_data.get('employeeID')).count() == 0:
			user = form.save()
			user.refresh_from_db()
			user.profile.usertype = form.cleaned_data.get('usertype')
			user.profile.employeeID = form.cleaned_data.get('employeeID')
			user.profile.group = form.cleaned_data.get('group')
			# print("usertype: " + form.cleaned_data.get('usertype'))
			user.profile.save()
			user.save()
		else:
			print('Error')
			print(User.objects.all().filter(username__iexact=form.cleaned_data.get('username')).count() == 0)
			print(User.objects.all().filter(email__iexact=form.cleaned_data.get('email')).count() == 0)
			print(Profile.objects.all().filter(employeeID__iexact=form.cleaned_data.get('employeeID')).count() == 0)
	return HttpResponseRedirect("/admin/")
	

@login_required(login_url="/login")	
def createGroup(request):
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid() and (Group.objects.all().filter(name__iexact=form.cleaned_data.get('name')).count() == 0):
			post = form.save(commit=False)
			post.save()
	return HttpResponseRedirect("/admin/")
	
	
	
	
	