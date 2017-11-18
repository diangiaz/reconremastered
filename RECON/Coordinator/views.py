from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import Context, RequestContext
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from . import forms
from .forms import SignUpForm
from .models import Group, Profile, Device, GroupToDevice, SaveTopology, SaveDev, SaveConn, Log
from django.db.models import Q
from time import sleep
from threading import Thread
import serial
import json
import datetime
import urllib.parse as urlparse

# Create your views here.
savedTopology = SaveTopology()

@login_required(login_url="/login")
def userPage(request):
	currentUser = request.user
	# if currentUser.profile.usertype == 'admin':
		# return HttpResponseRedirect("/admin/")

	groupTopologies = SaveTopology.objects.filter(group = currentUser.profile.group)
	users = User.objects.all()
	groups = Group.objects.all()
	devices = Device.objects.all()
	grouptodevice = GroupToDevice.objects.all()
	today=datetime.datetime.now().date()

	context = {
		'current_user': currentUser,
		'topologies': groupTopologies,
		'grouptodevice':grouptodevice,
		'devices':devices,
		'groups':groups,
		'users':users,
		'today':today
	}
	return render(request, 'user.html', context)
	
# serial reader/sender start
strBuilder1 = ""
# readState = False
# serialPort = serial.Serial("COM4", 9600)
# varCurr = ""
# varPrev = ""
		
# def Sender1():
	# global serialPort
	
	# while True:
		# serialPort.flushInput()
		# text = input("") + "\n"
		# serialPort.write(text.encode('utf-8'))
		# bytes_to_read = serialPort.inWaiting()
		# sleep(.2)
	
# class Receiver1(Thread):
		# def __init__(self, serialPort): 
			# Thread.__init__(self) 
			# self.serialPort = serialPort 
		# def run(self):
			# global serialPort
			# global strBuilder1
			# text = "" 
			# while (text != "exitReceiverThread\n"): 
				# text = serialPort.readline()
				# strBuilder1 += text.decode() + "\n"
				# print("serial output: " + text.decode())
			
			# self.serialPort.close()
			
# receive = Receiver1(serialPort) 
# receive.start()

# sSend1 = Thread(target=Sender1)
# sSend1.start()

def getSerialOutput1(request):
	global strBuilder1
	
	JSONer = {}
	JSONer['routerConfig'] = strBuilder1
	return HttpResponse(json.dumps(JSONer))
	
def sendSerial1(request):
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	text = (urlparse.parse_qs(parsedData.query)['routerInput'][0])
	
	audit = Log()
	audit.device = "Router"
	audit.user = request.user
	audit.action = text
	audit.save()	
	
	text += "\n"
	
	# serialPort.flushInput()
	# serialPort.write(text.encode('utf-8'))
	# bytes_to_read = serialPort.inWaiting()
	print(text)
	
	print("Audited " + audit.action + " @ time " + str(audit.timestamp))
	return HttpResponseRedirect(json.dumps(JSONer))

	
# serial reader/sender end	
	
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
		while ctr < GroupToDevice.objects.filter(device=deviceid).filter(type="AP").count() and success == True:
			arr1=GroupToDevice.objects.filter(device=deviceid).filter(type="AP").values_list('startDateTime', flat=True)
			#arr1[ctr].strftime("%Y-%m-%d")
			arr2=GroupToDevice.objects.filter(device=deviceid).filter(type="AP").values_list('endDateTime', flat=True)

			
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
			messages.success(request,"Device reserved, please wait for it to be confirmed!")
		else:
			messages.error(request,"The device is already reserved on those dates!")
		
	return HttpResponse(json.dumps(JSONer), context)		
	
@login_required(login_url="/login")
def loadTopology(request):
	currentUser = request.user
	if currentUser.profile.usertype == 'admin':
		return HttpResponseRedirect("/admin/")
		
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	topologyID = (urlparse.parse_qs(parsedData.query)['topologyID'][0])
	
	loadThisTopology = SaveTopology.objects.filter(id=topologyID)[0]
	print("Loaded " + loadThisTopology.name)
	
	groupTopologies = SaveTopology.objects.filter(group = currentUser.profile.group)
	users = User.objects.all()
	groups = Group.objects.all()
	devices = Device.objects.all()
	grouptodevice = GroupToDevice.objects.all()
	today=datetime.datetime.now().date()
	loadDevices = SaveDev.objects.filter(saveTopology = loadThisTopology)
	loadConnections = SaveConn.objects.filter(saveTopology = loadThisTopology)
	
	context = {
		'current_user': currentUser,
		'topologies': groupTopologies,
		'currTopology':loadThisTopology.name,
		'loadDevices': loadDevices,
		'connections': loadConnections,
		'grouptodevice':grouptodevice,
		'devices':devices,
		'groups':groups,
		'users':users,
		'today':today,
	}
	return render(request, 'user.html', context)
	
@login_required(login_url="/login")
def saveTopologyFunc(request):
	global savedTopology
	user = request.user

	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	topName = (urlparse.parse_qs(parsedData.query)['topologyName'][0])
	
	if (SaveTopology.objects.filter(name = topName).count() > 0):
		savedTopology = SaveTopology.objects.filter(name = topName)[0]
		SaveDev.objects.filter(saveTopology = savedTopology).delete()
		SaveConn.objects.filter(saveTopology = savedTopology).delete()
		print("Overwrite " + savedTopology.name)
	else:
		newTopology = SaveTopology()	
		newTopology.name = topName
		newTopology.group = user.profile.group
		newTopology.save()
		newTopology.refresh_from_db()
		savedTopology = newTopology
		print("Created " + newTopology.name)
		
	return HttpResponse(json.dumps(JSONer))
	
@login_required(login_url="/login")
def saveDevice(request):
	global savedTopology
	
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	devName = (urlparse.parse_qs(parsedData.query)['deviceName'][0])
	x = (urlparse.parse_qs(parsedData.query)['x'][0])
	y = (urlparse.parse_qs(parsedData.query)['y'][0])
	
	print("Save " + devName + " x/y=" + x + y + " to " + savedTopology.name)

	newSaveDev = SaveDev()
	newSaveDev.saveTopology = savedTopology
	newSaveDev.deviceName = devName
	newSaveDev.xCord = float(x)
	newSaveDev.yCord = float(y)
	newSaveDev.save()
		
	return HttpResponse(json.dumps(JSONer))

@login_required(login_url="/login")
def saveConnection(request):
	global savedTopology
	
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	connectionName = (urlparse.parse_qs(parsedData.query)['connectionName'][0])
	startX = (urlparse.parse_qs(parsedData.query)['startX'][0])	
	startY = (urlparse.parse_qs(parsedData.query)['startY'][0])
	endX = (urlparse.parse_qs(parsedData.query)['endX'][0])
	endY = (urlparse.parse_qs(parsedData.query)['endY'][0])
	srcDevice = (urlparse.parse_qs(parsedData.query)['srcDevice'][0])
	endDevice = (urlparse.parse_qs(parsedData.query)['endDevice'][0])
	srcPort = (urlparse.parse_qs(parsedData.query)['srcPort'][0])
	endPort = (urlparse.parse_qs(parsedData.query)['endPort'][0])
	
	print("Save " + connectionName + "src:" + srcDevice + " end:" + endDevice +" to " + savedTopology.name)
	
	if "LAN" in connectionName:
		cableType = 0
	elif "WAN" in connectionName:
		cableType = 1
	elif "CONSOLE" in connectionName:
		cableType = 2
	
	print("cable type is " + str(cableType))
	
	newSaveConn = SaveConn()
	newSaveConn.saveTopology = savedTopology
	newSaveConn.connectionName = connectionName
	newSaveConn.startX = float(startX)
	newSaveConn.startY = float(startY)
	newSaveConn.endX = float(endX)
	newSaveConn.endY = float(endY)
	newSaveConn.srcDevice = srcDevice
	newSaveConn.endDevice = endDevice
	newSaveConn.srcPort = srcPort
	newSaveConn.endPort = endPort
	newSaveConn.cableType = cableType
	newSaveConn.save()
	
	
	return HttpResponse(json.dumps(JSONer))

@login_required(login_url="/login")	
def adminPage(request):
	currentUser = request.user
	
	if currentUser.profile.usertype == 'employee':
		return HttpResponseRedirect("/user/")
	
	signupForm = SignUpForm()
	users = User.objects.all()	
	groups = Group.objects.all()
	grouptodevice = GroupToDevice.objects.all()
	devices = Device.objects.all()
	test = Group.objects.all()
	devicesort= Device.objects.all().order_by('name')
	today=datetime.datetime.now().date()
	valid = True
	
	context = {
	'groups':groups,
	'test':test,
	'today':today,
	'users':users,
	'current_user': currentUser,
	'signupForm' : signupForm,
	'grouptodevice' : grouptodevice,
	'devices':devices,
	'devicesort':devicesort,
	'valid':valid
	}
	return render(request, 'admin.html', context)
	
@login_required(login_url="/login")	
def createUser(request):
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	userName = (urlparse.parse_qs(parsedData.query)['userName'][0])
	firstName = (urlparse.parse_qs(parsedData.query)['firstName'][0])
	lastName = (urlparse.parse_qs(parsedData.query)['lastName'][0])
	email = (urlparse.parse_qs(parsedData.query)['email'][0])
	password = (urlparse.parse_qs(parsedData.query)['password'][0])
	employeeID = (urlparse.parse_qs(parsedData.query)['employeeID'][0])
	groupName = (urlparse.parse_qs(parsedData.query)['groupName'][0])
	
	newGroup = Group.objects.filter(name=groupName)[0]
	
	hashedPass = make_password(password)
	
	newUser = User()
	newUser.username = userName
	newUser.first_name = firstName
	newUser.last_name = lastName
	newUser.email = email
	newUser.password = hashedPass
	newUser.save()
	
	newUser.refresh_from_db()
	
	newUser.profile.usertype = "employee"
	newUser.profile.employeeID = employeeID
	newUser.profile.group = newGroup
	newUser.profile.save()
	newUser.save()
	
	
	
	return HttpResponse(json.dumps(JSONer))


@login_required(login_url="/login")	
def createGroup(request):
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	name = (urlparse.parse_qs(parsedData.query)['groupName'][0])
	
	grp = Group()
	grp.name = name
	grp.save()
	
	return HttpResponse(json.dumps(JSONer))
	
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
		print(grouptodeviceID.type)
		grouptodeviceID.save(force_update=True)
		messages.success(request,"Device reservation approved!")
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
		messages.success(request,"Device reservation declined!")
	return HttpResponse(json.dumps(JSONer))	

def deleteRes(request):		
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
		messages.success(request,"Device reservation removed!")
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
		while ctr < GroupToDevice.objects.filter(device=deviceid).filter(type="AP").count() and success == True:
			arr1=GroupToDevice.objects.filter(device=deviceid).filter(type="AP").values_list('startDateTime', flat=True)
			#arr1[ctr].strftime("%Y-%m-%d")
			arr2=GroupToDevice.objects.filter(device=deviceid).filter(type="AP").values_list('endDateTime', flat=True)

			
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
			messages.success(request,"Device reserved, please wait for it to be confirmed!")
		else:
			messages.error(request,"The device is already reserved on those dates!")
		
	return HttpResponse(json.dumps(JSONer), context)		

			
@login_required(login_url="/login")	
def allocateDevice(request):
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
		while ctr < GroupToDevice.objects.filter(device=deviceid).filter(type="AP").count() and success == True:
			arr1=GroupToDevice.objects.filter(device=deviceid).filter(type="AP").values_list('startDateTime', flat=True)
			#arr1[ctr].strftime("%Y-%m-%d")
			arr2=GroupToDevice.objects.filter(device=deviceid).filter(type="AP").values_list('endDateTime', flat=True)

			
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
			a = GroupToDevice(group=newgroupID,device=newdeviceID,startDateTime=startdate,endDateTime=enddate,type='AP')
			a.save()
			messages.success(request,"Successfully allocated!")
		else:
			messages.error(request,"Date already reserved!")

	return HttpResponse(json.dumps(JSONer), context)		
	
@login_required(login_url="/login")
def editModal(request):

	JSONer = {}
	valid = True
	parsedData = urlparse.urlparse(request.get_full_path())
	pkid = (urlparse.parse_qs(parsedData.query)['pkid'][0])
	idnum = (urlparse.parse_qs(parsedData.query)['id-num'][0])
	firstname = (urlparse.parse_qs(parsedData.query)['first-name'][0])
	lastname = (urlparse.parse_qs(parsedData.query)['last-name'][0])
	username = (urlparse.parse_qs(parsedData.query)['username'][0])
	email = (urlparse.parse_qs(parsedData.query)['email'][0])
	error_msg1 = "empty"
	error_msg2 = "empty"
	context = {
	'valid':valid,
	'error_msg1':error_msg1,
	'error_msg2':error_msg2,

	}
	

	if User.objects.filter(id=pkid).count() > 0:
		
		if Profile.objects.filter(Q(employeeID=idnum) & ~Q(user_id=pkid)).count() > 0:
			valid = False
			error_msg1 = "id is taken"
			print("id is already taken!")
		if User.objects.filter(Q(username = username) & ~Q(id=pkid)).count() > 0:
			valid = False
			error_msg2="username is taken"
			print("username is taken")
			messages.error(request,'Username is taken!',extra_tags="sameuser")
		if User.objects.filter(Q(email = email) & ~Q(id=pkid)).count() > 0:
			valid = False
			print("email is already taken!")
		if valid == False:
			response = HttpResponse(status=401)
			response['Content-Length'] = len(response.content)
			return response
		else:
			userID = User.objects.filter(id=pkid)[0]
			userID.profile.employeeID = idnum
			userID.first_name = firstname
			userID.last_name = lastname
			userID.username = username
			userID.email = email
			userID.save()
			messages.success(request,"Successfully updated account!")
		return HttpResponse(json.dumps(JSONer),context)


	return HttpResponse(json.dumps(JSONer),context)

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
		messages.success(request,"User successfully reassigned!")
	return HttpResponse(json.dumps(JSONer))	

