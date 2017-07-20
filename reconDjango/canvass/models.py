from django.db import models

class User(models.Models):
	ADMIN = 'Admin'
	EMPLOYEE = 'Employee'
	EMPLOYEE_TYPE_CHOICES = (
		(ADMIN, 'Admin'),
		(EMPLOYEE, 'Employee'),
	)
	username = models.CharField(
		max_length=25
	)
	password = models.CharField(
		max_length=25
	)
	name = models.CharField(
		max_length=50
	)
	email = models.EmailField(
		max_length=50
	)
	branch = models.CharField(
		max_length=50
	)
	usertype = models.CharField(
		max_length=10,
		choices=EMPLOYEE_TYPE_CHOICES,
	)
	idnum = models.IntegerField(
	)
	userID = models.AutoField(
		primary_key=true
	)
	
class Device(models.Models):
	ROUTER = 'Router'
	SWITCH = 'Switch'
	TERMINAL = 'Terminal'
	SERVER = 'Server'
	DEVICE_TYPE_CHOICES = (
		(ROUTER, 'Router'),
		(SWITCH, 'Switch'),
		(TERMINAL, 'Terminal'),
		(SERVER, 'Server'),
	)
	type = models.IntegerField(
		choices=DEVICE_TYPE_CHOICES
	)
	name = models.CharField(
		max_length=25
	)
	ycord = models.PositiveIntegerField(
	)
	xcord = models.PositiveIntegerField(
	)
	deviceID = models.AutoField(
		primary_key=true
	)

class Group(models.Models):
	groupname = models.CharField(
		max_length=25
	)
	groupID = models.AutoField(
		primary_key=true
	)

class Port(models.Models):
	SERIAL = 'Serial'
	GIGABYTE = 'Gigabyte'
	FASTETHERNET = 'Fast Ethernet'
	CONSOLE = 'Console'
	PORT_TYPE_CHOICES = (
		(SERIAL, 'Serial'),
		(GIGABYTE, 'Gigabyte'),
		(FASTETHERNET, 'Fast Ethernet'),
		(CONSOLE, 'Console'),
	)
	name = models.CharField(
		max_length=25
	)
	portID = models.AutoField(
		primary_key=true
	)
	type = models.CharField(
		max_length=20,
		choices=PORT_TYPE_CHOICES
	)
	deviceID = models.IntegerField(
		max_length=20
	)

class GroupToDevice(models.Models):
	RESERVE = 'RS'
	APPROVE = 'AP'
	ALLOCATION = 'AL'
	TYPE_CHOICES = (
		(RESERVE, 'Reserve'),
		(APPROVE, 'Approve'),
		(ALLOCATION, 'Allocation'),
	)
	groupID = models.IntegerField(
	)
	deviceId = models.IntegerField(
	)
	startDateTime = models.DateTimeField(
		auto_now=False,
		auto_now_add=False,
		)
	endDateTime = models.DateTimeField(
		auto_now=False,
		auto_now_add=False,
	)
	type = models.CharField(
		max_length = 2,
		choices = TYPE_CHOICES,
	)
	
class UserToGroup(models.Models):
	userID = models.IntegerField(
	)
	groupID	= models.IntegerField(
	)

class Connections(models.Models):
	CONSOLE = 'Console'
	SERIAL = 'Serial'
	STRAIGHT = 'Straight'
	CONNECTION_TYPE_CHOICES = (
		(CONSOLE, 'Console'),
		(SERIAL, 'Serial'),
		(STRAIGHT, 'Straight'),
	)
	groupID = models.IntegerField(
	)
	srcdevID = models.IntegerField(
	)
	srcdevPort = models.IntegerField(
	)
	destdevID = models.IntegerField(
	)
	destdevPort	= models.IntegerField(
	)
	cabletype = models.CharField(
		max_length=10,
		choices=CONNECTION_TYPE_CHOICES,
	)

class Config(models.Models):
	groupID = models.IntegerField(
	)
	devID = models.IntegerField(
	)
	config = models.FileField(
		upload_to=None,
		max_length=100,
	)
	configID = models.AutoField(
		primary_key=true
	)

class SaveTopology(models.Models):
	groupID = models.IntegerField(
	)
	name = models.CharField(
		max_length = 40
	)
	saveID = models.AutoField(
		primary_key=true
	)

class SaveConn(models.Models):
	CONSOLE = 'Console'
	SERIAL = 'Serial'
	STRAIGHT = 'Straight'
	CONNECTION_TYPE_CHOICES = (
		(CONSOLE, 'Console'),
		(SERIAL, 'Serial'),
		(STRAIGHT, 'Straight'),
	)
	saveID = models.AutoField(
		primary_key=true
	)
	srcdevID = models.IntegerField(
	)
	srcdevPort = models.IntegerField(
	)
	destdevID = models.IntegerField(
	)
	destdevPort = models.IntegerField(
	)
	cabletype = models.CharField(
		max_length=10,
		choices=CONNECTION_TYPE_CHOICES,
	)

class SaveDev(models.Models):
	saveID = models.AutoField(
		primary_key=true
	)
	xcord = models.IntegerField(
	)
	ycord = models.IntegerField(
	)
	devID = models.IntegerField(
	)


# Create your models here.
