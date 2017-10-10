from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from . import forms
from .forms import SignUpForm, CreateGroupForm, EditGroupForm
from .models import Group
# Create your views here.

import json
import urllib.parse as urlparse

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
		if form.is_valid():
			form.save()
			user = User.objects.filter(username = form.cleaned_data.get('username'))[0]
			user.usertype = form.cleaned_data.get('usertype')
			user.userID = form.cleaned_data.get('userID')
			# user.Profile.save()
			user.save()
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
	# JSONer = {}
	# JSONer['output'] = "Error: Invalid Input"

	# parsed = urlparse.urlparse(request.get_full_path())
	# userid = int(urlparse.parse_qs(parsed.query)['id'][0])

	# user = list(User.objects.all().filter(id=userid))[0]
	# print(user.id)
	# return HttpResponseRedirect("/admin/")
	# userfound = list(User.objects.all().filter(username=request.user.username))[0]
	
	if request.method == 'POST':
		# print(request)
		# for each in request:		
			# form = EditGroupForm(request.POST)
			
			pkid = request.POST.get('pkid')
			firstname = request.POST.get('first-name')
			lastname = request.POST.get('last-name')
			username = request.POST.get('user-name')
			email = request.POST.get('email')
			IDnum = request.POST.get('id-num')
			print(firstname, lastname, username, email, IDnum)

			if User.objects.filter(id=pkid).count() > 0:
				userID = User.objects.filter(id=pkid)[0]
				print(userID)
				print(userID.first_name)
				userID.Profile.userID = IDnum
				userID.first_name = firstname
				userID.last_name = lastname
				userID.username = username
				userID.email = email
				userID.save()
			
			# User.objects.filter(id=userID).update(username=username)
			# Profile.objects.select_related().filter(id=userID).update(userID = IDnum)
			# form.save()
			# post = form.save(commit=False
	return HttpResponseRedirect("/admin/")
	
	