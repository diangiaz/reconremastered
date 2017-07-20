from django.db import models

class User(models.Model):
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
		primary_key=True
	)
	
class Device(models.Model):
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
		primary_key=True
	)

class Group(models.Model):
	groupname = models.CharField(
		max_length=25
	)
	groupID = models.AutoField(
		primary_key=True
	)

class Port(models.Model):
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
		primary_key=True
	)
	type = models.CharField(
		max_length=20,
		choices=PORT_TYPE_CHOICES
	)
	deviceID = models.ForeignKey(
		'Device',
		on_delete=models.CASCADE,
	)
	

class GroupToDevice(models.Model):
	RESERVE = 'RS'
	APPROVE = 'AP'
	ALLOCATION = 'AL'
	TYPE_CHOICES = (
		(RESERVE, 'Reserve'),
		(APPROVE, 'Approve'),
		(ALLOCATION, 'Allocation'),
	)
	groupID = models.ForeignKey(
		'Group',
		on_delete=models.CASCADE,
	)
	deviceId = models.ForeignKey(
		'Device',
		on_delete=models.CASCADE,
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
	
class UserToGroup(models.Model):
	userID = models.ForeignKey(
		'User',
		on_delete=models.CASCADE,
	)
	groupID	= models.ForeignKey(
		'Group',
		on_delete=models.CASCADE,
	)

class Connections(models.Model):
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
	connectionID = models.AutoField(
		primary_key=True
	)

class Config(models.Model):
	groupID = models.ForeignKey(
		'Group',
		on_delete=models.CASCADE,
	)
	devID = models.ForeignKey(
		'Device',
		on_delete=models.CASCADE,
	)
	config = models.FileField(
		upload_to=None,
		max_length=100,
	)
	configID = models.AutoField(
		primary_key=True
	)

class SaveTopology(models.Model):
	groupID = models.IntegerField(
	)
	name = models.CharField(
		max_length = 40
	)
	saveID = models.AutoField(
		primary_key=True
	)

class SaveConn(models.Model):
	CONSOLE = 'Console'
	SERIAL = 'Serial'
	STRAIGHT = 'Straight'
	CONNECTION_TYPE_CHOICES = (
		(CONSOLE, 'Console'),
		(SERIAL, 'Serial'),
		(STRAIGHT, 'Straight'),
	)
	saveID = models.AutoField(
		primary_key=True
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

class SaveDev(models.Model):
	saveID = models.AutoField(
		primary_key=True
	)
	xcord = models.IntegerField(
	)
	ycord = models.IntegerField(
	)
	devID = models.IntegerField(
	)


# Create your models here.
