from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from . import forms
from .forms import SignUpForm
from .models import Group, Profile, SaveTopology
from time import sleep
from threading import Thread
import serial
import json
import urllib.parse as urlparse

# Create your views here.

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
	
	text += "\n"
	
	# serialPort.flushInput()
	# serialPort.write(text.encode('utf-8'))
	# bytes_to_read = serialPort.inWaiting()
	print(text)
	
	return HttpResponseRedirect(json.dumps(JSONer))

	
# serial reader/sender end

		

		
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
	
@login_required(login_url="/login")
def loadTopology(request):
	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	topologyID = (urlparse.parse_qs(parsedData.query)['topologyID'][0])
	
	currentTopology = SaveTopology.objects.filter(id=topologyID)[0]
	print("Loaded " + currentTopology.name)
	return HttpResponse(json.dumps(JSONer))	

	
@login_required(login_url="/login")
def saveTopologyFunc(request):
	user = request.user

	JSONer = {}
	parsedData = urlparse.urlparse(request.get_full_path())
	name = (urlparse.parse_qs(parsedData.query)['topologyName'][0])

	if (SaveTopology.objects.filter(name).count() > 0):
		name = name + "(copy)"
	
	
	newTopology = SaveTopology()	
	newTopology.name = name
	newTopology.group = user.profile.group
	newTopology.save()
	
	print("topology saved")
	
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
	
	newUser = User()
	newUser.username = userName
	newUser.first_name = firstName
	newUser.last_name = lastName
	newUser.email = email
	newUser.password = password
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