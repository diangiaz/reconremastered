from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from . import forms
from .forms import SignUpForm, CreateGroupForm
from .models import Group, Profile, Device, GroupToDevice

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
def userPage(request):
	currentUser = request.user
	
	if currentUser.profile.usertype == 'admin':
		return HttpResponseRedirect("/admin/")
	
	users = User.objects.all()	
	groups = Group.objects.all()
	devices = Device.objects.all()
	grouptodevice =GroupToDevice.objects.all()
	
	context = {
	'current_user': currentUser,
	'grouptodevice':grouptodevice,
	'devices':devices,
	'groups':groups,
	'users':users,
	}
	return render(request, 'user.html', context)
	
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
def reserveDevice(request):
	currentUser = request.user
	JSONer = {}	
	parsedData = urlparse.urlparse(request.get_full_path())
	pkid = (urlparse.parse_qs(parsedData.query)['pkid'][0])
	groupid = (urlparse.parse_qs(parsedData.query)['groupid'][0])
	startdate = (urlparse.parse_qs(parsedData.query)['start-date'][0])
	enddate = (urlparse.parse_qs(parsedData.query)['end-date'][0])
	deviceid = (urlparse.parse_qs(parsedData.query)['deviceList'][0])
	devicename = Device.objects.filter(id=deviceid)[0]
	devicename = devicename.name
	daterange1 = GroupToDevice.objects.filter(date__range=[startdate, enddate])

	
	if User.objects.filter(id=pkid).count() > 0 and Group.objects.filter(id=groupid).count() > 0:
			
		newgroupID = Group.objects.get(id=groupid)
		newdeviceID = Device.objects.get(id=deviceid)
		a = GroupToDevice(group=newgroupID,device=newdeviceID,startDateTime=startdate,endDateTime=enddate,type='RS')
		a.save()
			
		
	return HttpResponseRedirect(json.dumps(JSONer))

@login_required(login_url="/login")
def editModal(request):

	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	pkid = (urlparse.parse_qs(parsedData.query)['pkid'][0])
	idnum = (urlparse.parse_qs(parsedData.query)['id-num'][0])
	firstname = (urlparse.parse_qs(parsedData.query)['first-name'][0])
	lastname = (urlparse.parse_qs(parsedData.query)['last-name'][0])
	username = (urlparse.parse_qs(parsedData.query)['username'][0])
	email = (urlparse.parse_qs(parsedData.query)['email'][0])
	newid = (urlparse.parse_qs(parsedData.query)['newid'][0])

	if User.objects.filter(id=pkid).count() > 0:
	 	userID = User.objects.filter(id=pkid)[0]
	 	print(newid)
	 	userID.profile.employeeID = newid
	 	userID.first_name = firstname
	 	userID.last_name = lastname
	 	userID.username = username
	 	userID.email = email
	 	userID.save()
	
	return HttpResponseRedirect(json.dumps(JSONer))

@login_required(login_url="/login")	
def editGrp(request):		
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	pkid = (urlparse.parse_qs(parsedData.query)['pkid'][0])
	print(pkid)
	groupid = (urlparse.parse_qs(parsedData.query)['groupid'][0])
	if User.objects.filter(id=pkid).count() > 0 and Group.objects.filter(id=groupid).count() > 0:
		print(pkid)
		print(groupid)
		userID = User.objects.filter(id=pkid)[0]
		userID.profile.group_id = groupid
		print(userID.username)
		userID.save(force_update=True)
	return HttpResponseRedirect(json.dumps(JSONer))	
	
@login_required(login_url="/login")	
def createGroup(request):
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
	return HttpResponseRedirect("/admin/")

