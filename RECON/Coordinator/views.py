from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from . import forms
from .forms import SignUpForm, CreateGroupForm
from .models import Group, Profile, Device, GroupToDevice
import datetime
from datetime import timedelta
import json
import urllib.parse as urlparse
# Create your views here.





@login_required(login_url="/login")
def userPage(request):
	currentUser = request.user
	
	if currentUser.profile.usertype != 'employee':
		return HttpResponseRedirect("/admin/")

	users = User.objects.all()	
	context = {
		'current_user': currentUser
	}
	return render(request, 'user.html', context)

@login_required(login_url="/login")	
def adminPage(request):
	currentUser = request.user
	
	if currentUser.profile.usertype != 'admin':
		return HttpResponseRedirect("/user/")
	
	signupForm = SignUpForm()
	newgroupForm = CreateGroupForm()
	
	users = User.objects.all()	
	groups = Group.objects.all()
	grouptodevice = GroupToDevice.objects.all()
	
	
	context = {
	'groups':groups,
	'users':users,
	'current_user': currentUser,
	'newgroupForm': newgroupForm,
	'signupForm' : signupForm,
	'grouptodevice' : grouptodevice
	}
	return render(request, 'admin.html', context)

@login_required(login_url="/login")	
def userPage(request):
	currentUser = request.user
	
	if currentUser.profile.usertype != 'employee':
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
def approvedRes(request):		
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	print("check")
	print((urlparse.parse_qs(parsedData.query)['grouptodeviceid'][0]))
	pkid = (urlparse.parse_qs(parsedData.query)['grouptodeviceid'][0])
	print(pkid)
	
	if GroupToDevice.objects.filter(id=pkid).count() > 0:
		print(pkid)
	
		grouptodeviceID = GroupToDevice.objects.filter(id=pkid)[0]
		grouptodeviceID.type = "AP"
		
		grouptodeviceID.save(force_update=True)
	return HttpResponse(json.dumps(JSONer))	

def declinedRes(request):		
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	print("check")
	print((urlparse.parse_qs(parsedData.query)['grouptodeviceid'][0]))
	pkid = (urlparse.parse_qs(parsedData.query)['grouptodeviceid'][0])
	print(pkid)
	
	if GroupToDevice.objects.filter(id=pkid).count() > 0:
		print(pkid)
	
		grouptodeviceID = GroupToDevice.objects.filter(id=pkid)[0]
		grouptodeviceID.type = "DC"
		
		grouptodeviceID.save(force_update=True)
	return HttpResponse(json.dumps(JSONer))	

	
@login_required(login_url="/login")	
def reserveDevice(request):
	ctr = 0
	currentUser = request.user
	JSONer = {}	
	parsedData = urlparse.urlparse(request.get_full_path())
	pkid = (urlparse.parse_qs(parsedData.query)['pkid'][0])
	groupid = (urlparse.parse_qs(parsedData.query)['groupid'][0])
	startdate = (urlparse.parse_qs(parsedData.query)['start-date'][0])
	enddate = (urlparse.parse_qs(parsedData.query)['end-date'][0])
	deviceid = (urlparse.parse_qs(parsedData.query)['deviceList'][0])

	comparedate = datetime.datetime.strptime(startdate, "%Y-%m-%d").date()
	comparedate2 = datetime.datetime.strptime(enddate, "%Y-%m-%d").date()

	#daterange1 = GroupToDevice.objects.filter(date__range=[startdate, enddate])
	reservelist = GroupToDevice.objects.all()
	success = True
	ctr = 0
	context = {
	'success':success,
	}
	if User.objects.filter(id=pkid).count() > 0 and Group.objects.filter(id=groupid).count() > 0:
		devicename=Device.objects.filter(id=deviceid)[0]
		devicename = devicename.name
		while ctr < GroupToDevice.objects.filter(device=deviceid).count() and success == True:
			arr1=GroupToDevice.objects.filter(device=deviceid).values_list('startDateTime', flat=True)
			#arr1[ctr].strftime("%Y-%m-%d")
			arr2=GroupToDevice.objects.filter(device=deviceid).values_list('endDateTime', flat=True)

			
			if (comparedate >= arr1[ctr] and comparedate <= arr2[ctr]) or (comparedate2 >= arr1[ctr] and comparedate2 <= arr2[ctr]) or (arr1[ctr]  >= comparedate and arr1[ctr] <= comparedate2) or (arr2[ctr] >= comparedate and arr2[ctr] <= comparedate2):
			 	print("false")
			 	success = False
			else:
			 	print("true")
			 	success = True
			ctr = ctr+1
			
		
		if success == True:
			newgroupID = Group.objects.get(id=groupid)
			newdeviceID = Device.objects.get(id=deviceid)
			a = GroupToDevice(group=newgroupID,device=newdeviceID,startDateTime=startdate,endDateTime=enddate,type='RS')
			a.save()
		
	return HttpResponse(json.dumps(JSONer), context)		

			
		
	
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
	

	if User.objects.filter(id=pkid).count() > 0:
	 	userID = User.objects.filter(id=pkid)[0]
	
	 
	 	userID.profile.employeeID = idnum
	 	userID.first_name = firstname
	 	userID.last_name = lastname
	 	userID.username = username
	 	userID.email = email
	 	userID.save()
	
	return HttpResponse(json.dumps(JSONer))

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
	return HttpResponse(json.dumps(JSONer))	
	
@login_required(login_url="/login")	
def createGroup(request):
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()
	return HttpResponseRedirect("/admin/")

