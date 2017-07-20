from django.db import models

class User(models.Models):
	ADMIN 		= 'Admin'
	EMPLOYEE 	= 'Employee'
	EMPLOYEE_TYPE_CHOICES = (
		(ADMIN, 'Admin'),
		(EMPLOYEE, 'Employee'),
	)
	username 	= models.CharField(
		max_length=25,
		primary_key=true,
	)
	password 	= models.CharField(
		max_length=50
	)
	name		= models.CharField(
		max_length=50
	)
	email		= models.EmailField(
		max_length=254
	)
	branch		= models.CharField(
		max_length=50
	)
	usertype	= models.CharField(
		max_length=10,
		choices=EMPLOYEE_TYPE_CHOICES,
	)
	idnum		= models.IntegerField(
	)
	
class Device(models.Models):
	ROUTER 		= 'Router'
	SWITCH 		= 'Switch'
	TERMINAL 	= 'Terminal'
	SERVER 		= 'Server'
	DEVICE_TYPE_CHOICES = (
		(ROUTER, 'Router'),
		(SWITCH, 'Switch'),
		(TERMINAL, 'Terminal'),
		(SERVER, 'Server'),
	)
	type	= models.IntegerField(
		choices=DEVICE_TYPE_CHOICES
	)
	name	= models.CharField(
		max_length=50
	)
	ycord	= models.PositiveIntegerField(
	)
	xcord	= models.PositiveIntegerField(
	)

class Group(models.Models):
	groupname	= CharField(
		max_length=50,
		primary_key=true,
	)

class Port(models.Models):
	SERIAL 			= 'Serial'
	GIGABYTE 		= 'Gigabyte'
	FASTETHERNET	= 'Fast Ethernet'
	CONSOLE			= 'Console'
	PORT_TYPE_CHOICES = (
		(SERIAL, 'Serial'),
		(GIGABYTE, 'Gigabyte'),
		(FASTETHERNET, 'Fast Ethernet'),
		(CONSOLE, 'Console'),
	)
	name		= models.CharField(
		max_length=50
	)
	number		= IntegerField(
		primary_key=true
	)
	type		= models.CharField(
		max_length=20,
		choices=PORT_TYPE_CHOICES
	)
	deviceId	= models.CharField(
		max_length=20
	)

class GroupToDevice(models.Models):
	RESERVE 	= 'RS'
	APPROVE 	= 'AP'
	ALLOCATION 	= 'AL'
	TYPE_CHOICES = (
		(RESERVE, 'Reserve'),
		(APPROVE, 'Approve'),
		(ALLOCATION, 'Allocation'),
	)
	groupID		= CharField(
		max_length=50
	)
	deviceId	= CharField(
		max_length=50
	)
	startDateTime	= DateTimeField(
		auto_now=False,
		auto_now_add=False,
		)
	endDateTime		= DateTimeField(
		auto_now=False,
		auto_now_add=False,
	)
	type	= models.CharField(
		max_length = 2,
		choices = TYPE_CHOICES,
	)
	
class UserToGroup(models.Models):
	userID	= CharField(
		max_length=24
	)
	groupID	= CharField(
		max_length=50
	)

class Connections(models.Models):
	groupID		= CharField(
		max_length=50
	)
	srcdevID	= CharField(
		max_length=50
	)
	srcdevPort	= 
	destdevID
	destdevPort
	cabletype

class Config(models.Models):
	groupID
	devID
	config

class SaveTopology(models.Models):
	groupID
	name

class SaveConn(models.Models):
	saveID
	srcdevID
	srcdevPort
	destdevID
	destdevPort
	cabletype

class SaveDev(models.Models):
	saveID
	type
	name
	xcord
	ycord


# Create your models here.
