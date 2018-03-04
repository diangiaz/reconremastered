from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import Context, RequestContext
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core import serializers
from . import forms
from .forms import SignUpForm
from .models import Group, Profile, Device, GroupToDevice, SaveTopology, SaveDev, SaveConn, Log, Port, Comport, MainSwitchPort
from django.db.models import Q
from time import sleep
from threading import Thread
import serial
import json
import datetime
import urllib.parse as urlparse

# Create your views here.
# fill comports and mainswitchports

comports = Comport.objects.all().count()
x = 5
if comports == 0:
	while x <= 6:
		c = Comport()
		c.name = "COM" + str(x)
		c.save()
		print("added" + str(c))
		x+=1

mainswitchports = MainSwitchPort.objects.all().count()
x = 1
if mainswitchports == 0:
	while x <= 24:
		m = MainSwitchPort()
		m.name = "fa0/" + str(x)
		m.save()
		print("added" + str(m))
		x+=1
		
	nDevice = Device()
	nDevice.type = 'Router'
	nDevice.name = 'Router 1'
	nDevice.comport = Comport.objects.filter(name = 'COM5')[0]
	nDevice.save()
	nDevice2 = Device()
	nDevice2.type = 'Switch'
	nDevice2.name = 'Switch 1'
	nDevice2.comport = Comport.objects.filter(name = 'COM6')[0]
	nDevice2.save()
	p1 = Port()
	p1.type = 'Fast Ethernet'
	p1.name = 'fa0/0'
	p1.device = nDevice
	p1.mainswitchport = MainSwitchPort.objects.filter(name = 'fa0/1')[0]
	p1.save()
	p2 = Port()
	p2.type = 'Fast Ethernet'
	p2.name = 'fa0/1'
	p2.device = nDevice
	p2.mainswitchport = MainSwitchPort.objects.filter(name = 'fa0/2')[0]
	p2.save()
	p3 = Port()
	p3.type = 'Fast Ethernet'
	p3.name = 'fa0/1'
	p3.device = nDevice2
	p3.mainswitchport = MainSwitchPort.objects.filter(name = 'fa0/3')[0]
	p3.save()
	p4 = Port()
	p4.type = 'Fast Ethernet'
	p4.name = 'fa0/2'
	p4.device = nDevice2
	p4.mainswitchport = MainSwitchPort.objects.filter(name = 'fa0/4')[0]
	p4.save()
	p5 = Port()
	p5.type = 'Fast Ethernet'
	p5.name = 'fa0/3'
	p5.device = nDevice2
	p5.mainswitchport = MainSwitchPort.objects.filter(name = 'fa0/5')[0]
	p5.save()
	p6 = Port()
	p6.type = 'Fast Ethernet'
	p6.name = 'fa0/4'
	p6.device = nDevice2
	p6.mainswitchport = MainSwitchPort.objects.filter(name = 'fa0/6')[0]
	p6.save()
	
@login_required(login_url="/login")
def userPage(request):
	currentUser = request.user
	if currentUser.profile.usertype == 'admin':
		return HttpResponseRedirect("/admin/")

	groupTopologies = SaveTopology.objects.filter(group = currentUser.profile.group)
	users = User.objects.all()
	groups = Group.objects.all()
	devices = Device.objects.all()
	grouptodevice = GroupToDevice.objects.all()
	today=datetime.datetime.now().date()
	ports = Port.objects.all()

	context = {
		'current_user': currentUser,
		'topologies': groupTopologies,
		'grouptodevice':grouptodevice,
		'devices':devices,
		'groups':groups,
		'users':users,
		'today':today,
		'ports':ports,
	}
	return render(request, 'user.html', context)

# create serial connections
	
class Receiver(Thread):
		def __init__(self, Serial, Idx):
			Thread.__init__(self) 
			self.serialPort = Serial
			self.index = Idx
		def run(self):
			text = "" 
			while (text != "exitReceiverThread\n"): 
				text = self.serialPort.readline()
				strBuilders[self.index] += text.decode() + "\n"
			
			self.serialPort.close()		
	
devices = Device.objects.all()

strBuilders = []
serialList = []
receiverList = []
			
try:
	mainSwitchSerial = serial.Serial('COM7', 9600)
except serial.SerialException:
	print("Main switch not detected")

for idx, device in enumerate(devices):
	try:
		cereal = serial.Serial(device.comport.name, 9600)
		strBuilders.append("")
		serialList.append(cereal)
	except serial.SerialException:
		print("comport not detected")
		
	device.serialIndex = idx
	device.save()
	
for idx, serial in enumerate(serialList):
	r = Receiver(serial, idx)
	receiverList.append(r)

for idx, receiver in enumerate(receiverList):
	receiver.start()

# create serial connections end	
	
def inputSend(request):
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	text = (urlparse.parse_qs(parsedData.query)['input'][0])
	deviceID = (urlparse.parse_qs(parsedData.query)['deviceId'][0])
	
	device = Device.objects.filter(id = deviceID)[0]
	
	# if (text != "return"):	
		# audit = Log()
		# audit.device = device
		# audit.user = request.user
		# audit.action = text
		# audit.save()
		# print("Audited " + audit.action + " @ time " + str(audit.timestamp))
	
	text += "\n\n"
	
	if (text == "return\n\n"):
		text = "\r"
	
	serialList[device.serialIndex].flushInput()
	serialList[device.serialIndex].write(text.encode('utf-8'))
	bytes_to_read = serialList[device.serialIndex].inWaiting()
	
	print(text)

	return HttpResponseRedirect(json.dumps(JSONer))

def getSerialOutput(request):
	return JsonResponse(strBuilders, safe=False)

def getPorts(request):
	parsedData = urlparse.urlparse(request.get_full_path())
	devicename = (urlparse.parse_qs(parsedData.query)['device'][0])
	
	device = Device.objects.filter(name = devicename)[0]
	ports = Port.objects.filter(device = device).filter(istaken = '0')
	
	data = serializers.serialize('json', ports, fields=('name'))
	
	return JsonResponse(data, safe=False)	
	
@login_required(login_url="/login")
def connectDevices(request):
	global mainSwitchSerial

	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	srcDevice = (urlparse.parse_qs(parsedData.query)['srcDevice'][0])
	endDevice = (urlparse.parse_qs(parsedData.query)['endDevice'][0])
	srcPort = (urlparse.parse_qs(parsedData.query)['srcPort'][0])
	endPort = (urlparse.parse_qs(parsedData.query)['endPort'][0])
	
	device1 = Device.objects.filter(name = srcDevice)[0]
	device2 = Device.objects.filter(name = endDevice)[0]
	
	port1 = Port.objects.filter(name = srcPort).filter(device = device1)[0]
	port2 = Port.objects.filter(name = endPort).filter(device = device2)[0]
	
	port1.istaken = "1"
	port2.istaken = "1"
	
	# port1.save()
	# port2.save()
	
	print(port1.istaken)
	print(port2.istaken)
	
	p1 = str(port1.mainswitchport)
	p2 = str(port2.mainswitchport)

	vlan1 = "10" + p1.split("/",1)[1]
	
	text = "\renable\nconfigure terminal\ninterface range " + p1 +", " + p2 +"\nswitchport mode access\nswitchport access vlan " + vlan1 + "\nexit"	
	print(text)
	print("connected devices")
	mainSwitchSerial.flushInput()
	mainSwitchSerial.write(text.encode('utf-8'))
	bytes_to_read = mainSwitchSerial.inWaiting()
	
	return JsonResponse(JSONer)
	
@login_required(login_url="/login")
def disconnectDevices(request):
	global mainSwitchSerial
	
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	srcDevice = (urlparse.parse_qs(parsedData.query)['srcDevice'][0])
	endDevice = (urlparse.parse_qs(parsedData.query)['endDevice'][0])
	srcPort = (urlparse.parse_qs(parsedData.query)['srcPort'][0])
	endPort = (urlparse.parse_qs(parsedData.query)['endPort'][0])
	
	device1 = Device.objects.filter(name = srcDevice)[0]
	device2 = Device.objects.filter(name = endDevice)[0]
	
	port1 = Port.objects.filter(name = srcPort).filter(device = device1)[0]
	port2 = Port.objects.filter(name = endPort).filter(device = device2)[0]
	
	port1.istaken = "0"
	port2.istaken = "0"
	
	# port1.save()
	# port2.save()

	p1 = str(port1.mainswitchport)
	p2 = str(port2.mainswitchport)

	vlan1 = "10" + p1.split("/",1)[1]
	vlan2 = "10" + p2.split("/",1)[1]
	
	text = "\renable\nconfigure terminal\ninterface " + p1 +"\nswitchport mode access\nswitchport access vlan " + vlan1 + "\nexit"	
	text += "\renable\nconfigure terminal\ninterface " + p2 +"\nswitchport mode access\nswitchport access vlan " + vlan2 + "\nexit"	
	print(text)
	print("Disconnected devices")
	mainSwitchSerial.flushInput()
	mainSwitchSerial.write(text.encode('utf-8'))
	bytes_to_read = mainSwitchSerial.inWaiting()	
	
	return JsonResponse(JSONer)
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
	load = (urlparse.parse_qs(parsedData.query)['newload'][0])
	
	loadThisTopology = SaveTopology.objects.filter(id=topologyID)[0]
	print("loaded")
	
	groupTopologies = SaveTopology.objects.filter(group = currentUser.profile.group)
	users = User.objects.all()
	groups = Group.objects.all()
	devices = Device.objects.all()
	grouptodevice = GroupToDevice.objects.all()
	today=datetime.datetime.now().date()
	loadDevices = SaveDev.objects.filter(saveTopology = loadThisTopology)
	connections = SaveConn.objects.filter(saveTopology = loadThisTopology)
	
	loadConnections(connections)
	
	context = {
		'current_user': currentUser,
		'topologies': groupTopologies,
		'currTopology':loadThisTopology.name,
		'currTopologyID':topologyID,
		'loadDevices': loadDevices,
		'connections': connections,
		'grouptodevice':grouptodevice,
		'devices':devices,
		'groups':groups,
		'users':users,
		'today':today,
		'load':load,
	}
	return render(request, 'user.html', context)
	
@login_required(login_url="/login")
def saveTopologyFunc(request):
	user = request.user

	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	topName = (urlparse.parse_qs(parsedData.query)['topologyName'][0])
	
	if (SaveTopology.objects.filter(name = topName).count() > 0):
		savedTopology = SaveTopology.objects.filter(name = topName)[0]
		SaveDev.objects.filter(saveTopology = savedTopology).delete()
		SaveConn.objects.filter(saveTopology = savedTopology).delete()
		JSONer['tId'] = savedTopology.pk
		print("Overwrite " + savedTopology.name)
	else:
		newTopology = SaveTopology()	
		newTopology.name = topName
		newTopology.group = user.profile.group
		newTopology.save()
		newTopology.refresh_from_db()
		print("Created " + newTopology.name)
		JSONer['tId'] = newTopology.pk
		
	return HttpResponse(json.dumps(JSONer))
	
@login_required(login_url="/login")
def saveDevice(request):
	
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	devName = (urlparse.parse_qs(parsedData.query)['deviceName'][0])
	x = (urlparse.parse_qs(parsedData.query)['x'][0])
	y = (urlparse.parse_qs(parsedData.query)['y'][0])
	tId = (urlparse.parse_qs(parsedData.query)['tId'][0])
	savedTopology = SaveTopology.objects.filter(id=tId)[0]
	deviceID = Device.objects.filter(name = devName)[0]
	deviceID = deviceID.id
	gtd = GroupToDevice.objects.filter(device = deviceID)[0]
	print("Save " + devName + " x/y=" + x + y + " to " + savedTopology.name)

	newSaveDev = SaveDev()
	newSaveDev.saveTopology = savedTopology
	newSaveDev.GroupToDevice = gtd
	newSaveDev.deviceName = devName
	newSaveDev.xCord = float(x)
	newSaveDev.yCord = float(y)
	newSaveDev.save()
		
	return HttpResponse(json.dumps(JSONer))

@login_required(login_url="/login")
def saveConnection(request):
	
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
	tId = (urlparse.parse_qs(parsedData.query)['tId'][0])
	savedTopology = SaveTopology.objects.filter(id=tId)[0]
	
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
	log = Log.objects.all()
	comport = Comport.objects.all()
	mainswitchports = MainSwitchPort.objects.all()
	
	valid = True
	error_msg1 = ""
	
	routerCount = Device.objects.filter(type = 'Router').count()
	switchCount = Device.objects.filter(type = 'Switch').count()
	terminalCount = Device.objects.filter(type = 'Siwtch').count()
	
	context = {
	'log':log,
	'groups':groups,
	'test':test,
	'today':today,
	'users':users,
	'current_user': currentUser,
	'signupForm' : signupForm,
	'grouptodevice' : grouptodevice,
	'devices':devices,
	'devicesort':devicesort,
	'valid':valid,
	'error_msg1':error_msg1,
	'routerCount':routerCount,
	'switchCount':switchCount,
	'terminalCount':terminalCount,
	'comport':comport,
	'mainswitchports':mainswitchports,
	}
	return render(request, 'admin.html', context)
	
@login_required(login_url="/login")	
def createUser(request):
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	signupformisvalid = True
	signupUsererr = ""
	signupIDerr = ""
	signupEmailerr = ""
	signupPasserr = ""
	signupPasserr2 = ""
	signupFirstnameerr = ""
	signupLastnameerr = ""
	employeeID = ""
	firstName = ""
	lastName = ""
	email = ""
	password = ""
	password2 = ""
	userName = ""
	try:
		employeeID = (urlparse.parse_qs(parsedData.query)['employeeID'][0])
	except KeyError:
		signupformisvalid = False
		signupIDerr = "This field is required!"
	try:
		firstName = (urlparse.parse_qs(parsedData.query)['firstName'][0])
	except KeyError:
		signupformisvalid = False
		signupFirstnameerr = "This field is required!"
	try:
		lastName = (urlparse.parse_qs(parsedData.query)['lastName'][0])
	except KeyError:
		signupformisvalid = False
		signupLastnameerr = "This field is required!"
	try:
		userName = (urlparse.parse_qs(parsedData.query)['userName'][0])
	except KeyError:
		signupformisvalid = False
		signupUsererr = "This field is required!"
	try:
		email = (urlparse.parse_qs(parsedData.query)['email'][0])
	except KeyError:
		signupformisvalid = False
		signupEmailerr = "This field is required!"
	try:
		password = (urlparse.parse_qs(parsedData.query)['password'][0])
	except KeyError:
		signupformisvalid = False
		signupPasserr = "This field is required!"
	try:
		password2 = (urlparse.parse_qs(parsedData.query)['password2'][0])
	except KeyError:
		signupformisvalid = False
		signupPasserr2 = "This field is required!"
		
	groupName = (urlparse.parse_qs(parsedData.query)['groupName'][0])
	newGroup = Group.objects.filter(name=groupName)[0]
	
	print(employeeID)
	
	if(User.objects.filter(username = userName).count() > 0 ):
		signupUsererr = "Username is taken"
		signupformisvalid = False
		
	if(Profile.objects.filter(employeeID = employeeID).count() > 0 ):
		signupIDerr = "Employee ID is taken"
		signupformisvalid = False
	
	if(User.objects.filter(email = email).count() > 0 ):
		signupEmailerr = "Email is taken"
		signupformisvalid = False
		
	if(password != password2):
		signupPasserr2 = "Passwords do not match"
		signupformisvalid = False
	
	try: 
		validate_email(email)	
	except:
		if not signupEmailerr:
			signupformisvalid = False
			signupEmailerr = "Email is invalid!"
		
	context = {
		'signupformisvalid':signupformisvalid,
		'signupUsererr':signupUsererr,
		'signupIDerr':signupIDerr,
		'signupEmailerr':signupEmailerr,
		'signupPasserr':signupPasserr,
		'signupPasserr2':signupPasserr2,
	}
	
	if signupformisvalid == False:
		JSONer['signupformisvalid'] =  signupformisvalid
		JSONer['signupUsererr'] = signupUsererr
		JSONer['signupIDerr'] = signupIDerr
		JSONer['signupEmailerr'] = signupEmailerr
		JSONer['signupPasserr'] = signupPasserr
		JSONer['signupPasserr2'] = signupPasserr2
		JSONer['signupFirstnameerr'] = signupFirstnameerr
		JSONer['signupLastnameerr'] = signupLastnameerr
		
		return HttpResponse(json.dumps(JSONer), context)
	
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
	messages.success(request,"User created!")
	return HttpResponse(json.dumps(JSONer))

@login_required(login_url="/login")	
def createGroup(request):
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	name = (urlparse.parse_qs(parsedData.query)['groupName'][0])
	
	groupnameisvalid = True
	groupnameerrormessage = ""
	
	if(Group.objects.filter(name = name).count() > 0 ):
		groupnameerrormessage = "Group name is taken"
		groupnameisvalid = False
		
	if(name == ""):
		groupnameerrormessage = "Group name is required"
		groupnameisvalid = False
		
	context = {
		'groupnameisvalid':groupnameisvalid,
		'groupnameerrormessage':groupnameerrormessage,
	}
	
	if groupnameisvalid == False:
		JSONer['groupnameisvalid'] =  groupnameisvalid
		JSONer['groupnameerrormessage'] = groupnameerrormessage
		
		return HttpResponse(json.dumps(JSONer), context)
	messages.success(request,"Group successfully created!")
	grp = Group()
	grp.name = name
	grp.save()
	
	return HttpResponse(json.dumps(JSONer), context)

@login_required(login_url="/login")	
def approvedRes(request):		
	JSONer = {}
	ctr = 0
	parsedData = urlparse.urlparse(request.get_full_path())
	print("check")
	print((urlparse.parse_qs(parsedData.query)['grouptodeviceid'][0]))
	pkid = (urlparse.parse_qs(parsedData.query)['grouptodeviceid'][0])
	print(pkid)
	success = True
	context = {
	'success':success,
	}
	
	if GroupToDevice.objects.filter(id=pkid).count() > 0:
		print(pkid)
	
		grouptodeviceID = GroupToDevice.objects.filter(id=pkid)[0]
		deviceid = grouptodeviceID.device.id
		comparedate = grouptodeviceID.startDateTime
		comparedate2 = grouptodeviceID.endDateTime

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
			grouptodeviceID.type = "AP"
			print(grouptodeviceID.type)
			grouptodeviceID.save(force_update=True)
			messages.success(request,"Device reservation approved!")
		else:
			grouptodeviceID.type = "DC"
			grouptodeviceID.save(force_update=True)
			messages.error(request,"The device is already reserved on that day, device reservation removed!")

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
	error_id = ""
	error_first = ""
	error_last = ""
	error_user = ""
	error_email = ""
	username = ""
	firstname = ""
	lastname = ""
	email = ""
	idnum = ""
	
	context = {
	'valid':valid,
	'error_id':error_id,
	'error_first':error_first,
	'error_last':error_last,
	'error_user':error_user,
	'error_email':error_email,
	}

	parsedData = urlparse.urlparse(request.get_full_path())
	
	pkid = (urlparse.parse_qs(parsedData.query)['pkid'][0])
	try:
		idnum = (urlparse.parse_qs(parsedData.query)['id-num'][0])
	except KeyError:
		valid = False
		error_id = "This field is required!"
	try:
		firstname = (urlparse.parse_qs(parsedData.query)['first-name'][0])
	except KeyError:
		valid = False
		error_first = "This field is required!"
	try:
		lastname = (urlparse.parse_qs(parsedData.query)['last-name'][0])
	except KeyError:
		valid = False
		error_last = "This field is required!"
	try:
		username = (urlparse.parse_qs(parsedData.query)['username'][0])
	except KeyError:
		valid = False
		error_user = "This field is required!"
	try:
		email = (urlparse.parse_qs(parsedData.query)['email'][0])
	except KeyError:
		valid = False
		error_email = "This field is required!"

	if User.objects.filter(id=pkid).count() > 0:
		

		if Profile.objects.filter(Q(employeeID=idnum) & ~Q(user_id=pkid)).count() > 0:
			valid = False
			error_id = "id is taken"
			print("id is already taken!")
		if User.objects.filter(Q(username = username) & ~Q(id=pkid)).count() > 0:
			valid = False
			error_user ="username is taken"
			print("username is taken")
			#messages.error(request,'Username is taken!',extra_tags="sameuser")
		try: 
			validate_email(email)
			if User.objects.filter(Q(email = email) & ~Q(id=pkid)).count() > 0:
				valid = False
				error_email = "email is already taken!"
				print("email is already taken!")
		except:
			valid = False
			if not error_email:
				error_email = "email is invalid!"
		
		if valid == False:
		 	
		 	JSONer['valid'] = valid
		 	JSONer['error_id'] = error_id
		 	JSONer['error_first'] = error_first
		 	JSONer['error_last'] = error_last
		 	JSONer['error_user'] = error_user
		 	JSONer['error_email'] = error_email
		 	
		 	return HttpResponse(json.dumps(JSONer),context)

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

def addDevice(request):
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	type = (urlparse.parse_qs(parsedData.query)['type'][0])
	comportname = (urlparse.parse_qs(parsedData.query)['comport'][0])
	comport = Comport.objects.filter(name=comportname)[0]
	
	if type == '2':
		portNumber = (urlparse.parse_qs(parsedData.query)['portnumber'][0])
		mainswitchports = []
		portactivity = []
		if portNumber == '12':
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p1'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p2'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p3'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p4'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p5'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p6'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p7'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p8'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p9'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p10'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p11'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p12'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f1'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f2'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f3'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f4'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f5'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f6'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f7'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f8'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f9'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f10'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f11'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f12'][0]))
			print(mainswitchports)
		elif portNumber == '24':
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p1'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p2'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p3'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p4'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p5'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p6'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p7'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p8'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p9'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p10'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p11'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p12'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p13'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p14'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p15'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p16'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p17'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p18'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p19'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p20'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p21'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p22'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p23'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p24'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f1'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f2'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f3'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f4'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f5'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f6'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f7'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f8'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f9'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f10'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f11'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f12'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f13'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f14'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f15'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f16'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f17'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f18'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f19'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f20'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f21'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f22'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f23'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f24'][0]))
			print(mainswitchports)
		elif portNumber == '48':
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p1'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p2'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p3'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p4'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p5'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p6'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p7'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p8'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p9'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p10'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p11'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p12'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p13'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p14'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p15'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p16'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p17'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p18'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p19'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p20'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p21'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p22'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p23'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p24'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p25'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p26'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p27'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p28'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p29'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p30'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p31'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p32'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p33'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p34'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p35'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p36'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p37'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p38'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p39'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p40'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p41'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p42'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p43'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p44'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p45'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p46'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p47'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['p48'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f1'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f2'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f3'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f4'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f5'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f6'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f7'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f8'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f9'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f10'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f11'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f12'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f13'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f14'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f15'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f16'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f17'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f18'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f19'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f20'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f21'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f22'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f23'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f24'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f25'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f26'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f27'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f28'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f29'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f30'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f31'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f32'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f33'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f34'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f35'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f36'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f37'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f38'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f39'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f40'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f41'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f42'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f43'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f44'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f45'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f46'][0]))
			portactivity.append((urlparse.parse_qs(parsedData.query)['f47'][0]))
			mainswitchports.append((urlparse.parse_qs(parsedData.query)['f48'][0]))

		nDevice = Device()
		nDevice.type = 'Switch'
		nDevice.name = 'Switch ' + str(Device.objects.filter(type='Switch').count() + 1)
		nDevice.comport = comport
		# nDevice.save()  
		
		comport.istaken = '1'
		# comport.save()
		
		for idx, port in enumerate(mainswitchports):
			nPort = Port()
			nPort.name='fa0/' + str(idx+1)
			nPort.type = 'Fast Ethernet'
			nPort.device = nDevice
			mps = MainSwitchPort.objects.filter(pk=port)[0]
			mps.istaken = '1'
			# mps.save()
			nPort.mainswitchport = mps
			if portactivity[idx] == 'true':
				nPort.isactive = '1'
			# nPort.save()
		
		# AddSerialConnection(comport, nDevice)
		
		print(mainswitchports)
		if len(mainswitchports) > len(set(mainswitchports)):
			print('not unique')
		else:
			print('unique')
	
	if type == '1':
		mainswitchports = []
		portactivity = []
		nDevice = Device()
		nDevice.type = 'Router'
		nDevice.name = 'Router ' + str(Device.objects.filter(type='Router').count() + 1)
		nDevice.comport = comport
		# nDevice.save()
		
		comport.istaken = '1'
		# comport.save()
		
		mainswitchports.append((urlparse.parse_qs(parsedData.query)['rp1'][0]))
		mainswitchports.append((urlparse.parse_qs(parsedData.query)['rp2'][0]))
		
		for idx, port in enumerate(mainswitchports):
			nPort = Port()
			nPort.name='fa0/' + str(idx+1)
			nPort.type = 'Fast Ethernet'
			nPort.device = nDevice
			mps = MainSwitchPort.objects.filter(pk=port)[0]
			mps.istaken = '1'
			# mps.save()
			nPort.mainswitchport = mps
			nPort.isactive = '1'
			# nPort.save()
		
		AddSerialConnection(comport, nDevice)
		
		# unique port checker
		# if len(mainswitchports) > len(set(mainswitchports)):
			# print('not unique')
		# else:
			# print('unique')

	return HttpResponse(json.dumps(JSONer))

def AddSerialConnection(comport, device):
	
	try:
		cereal = serial.Serial(str(comport), 9600)
		idx = len(serialList)
		serialList.append(cereal)
		strBuilders.append("")
		d = Device.objects.filter(name='device')[0]
		d.serialIndex = idx
		# d.save()
		r = Receiver(cereal, idx)
		receiverList.append(r)
		r.start()
	except serial.SerialException:
		print("Serial is not detected")

def loadConnections(connections):
	for connection in connections:
		d1 = Device.objects.filter(name = connection.srcDevice)[0]
		d2 = Device.objects.filter(name = connection.endDevice)[0]
		p1 = Port.objects.filter(device = d1).filter(name = connection.srcPort)[0]
		p2 = Port.objects.filter(device = d2).filter(name = connection.endPort)[0]
		
		p1.istaken = "1"
		p2.istaken = "1"
		
		# p1.save()
		# p2.save()
		
		ps1 = str(p1.mainswitchport)
		ps2 = str(p2.mainswitchport)
		
		vlan1 = "10" + p1.split("/",1)[1]
	
		text = "\renable\nconfigure terminal\ninterface range " + p1 +", " + p2 +"\nswitchport mode access\nswitchport access vlan " + vlan1 + "\nexit"	
		print(text)
		print("connected devices")
		mainSwitchSerial.flushInput()
		mainSwitchSerial.write(text.encode('utf-8'))
		bytes_to_read = mainSwitchSerial.inWaiting()
	

	print("load that shit")

def removeConnections():
	connections = Port.objects.all()
	for connection in connections:
		connection.istaken = '0'
		connection.save()