from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import Context, RequestContext
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from . import forms
from .forms import SignUpForm
from .models import Group, Profile, SaveTopology, SaveDev, SaveConn, Log
from time import sleep
from threading import Thread
import serial
import json
import urllib.parse as urlparse

# Create your views here.
savedTopology = SaveTopology()

@login_required(login_url="/login")
def userPage(request):
	currentUser = request.user
	groupTopologies = SaveTopology.objects.filter(group = currentUser.profile.group)
	
	
	if currentUser.profile.usertype == 'admin':
		return HttpResponseRedirect("/admin/")

	users = User.objects.all()	
	context = {
		'current_user': currentUser,
		'topologies': groupTopologies,
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
	loadDevices = SaveDev.objects.filter(saveTopology = loadThisTopology)
	loadConnections = SaveConn.objects.filter(saveTopology = loadThisTopology)
	
	
	context = {
		'current_user': currentUser,
		'topologies': groupTopologies,
		'currTopology':loadThisTopology.name,
		'devices': loadDevices,
		'connections': loadConnections
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
	
	
	context = {
	'users':users,
	'groups':groups,
	'current_user': currentUser,
	'signupForm' : signupForm,
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