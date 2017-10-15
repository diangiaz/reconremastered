from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from . import forms
from .forms import SignUpForm, CreateGroupForm, EditGroupForm
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
	editgroupForm = EditGroupForm()
	users = User.objects.all()	
	groups = Group.objects.all()
	
	
	context = {
	'groups':groups,
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
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
	return HttpResponseRedirect("/admin/")
	
@login_required(login_url="/login")	
def editModal(request):		
	if request.method == 'POST':
		pkid = request.POST.get('pkid')
		firstname = request.POST.get('first-name')
		lastname = request.POST.get('last-name')
		username = request.POST.get('user-name')
		email = request.POST.get('email')
		IDnum = request.POST.get('id-num')
		if User.objects.filter(id=pkid).count() > 0:
			userID = User.objects.filter(id=pkid)[0]
			userID.profile.employeeID = IDnum
			userID.first_name = firstname
			userID.last_name = lastname
			userID.username = username
			userID.email = email
			userID.save()
	return HttpResponseRedirect("/admin/")

@login_required(login_url="/login")	
def editGrp(request):		
	if request.method == 'POST':
		pkid = request.POST.get('employeeName')
		groupid = request.POST.get('groupid')
		print(groupid)
		print(pkid)
		if User.objects.filter(id=pkid).count() > 0 and Group.objects.filter(id=groupid).count() > 0:
			userID = User.objects.filter(id=pkid)[0]
			print(userID.profile.group.id)
			userID.profile.group_id = groupid
			print(userID.profile.group_id)
			print(userID.username)
			userID.save(force_update=True)
	return HttpResponseRedirect("/admin/")
	
	