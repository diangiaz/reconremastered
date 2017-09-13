from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
	ADMIN = 'Admin'
	EMPLOYEE = 'Employee'
	EMPLOYEE_TYPE_CHOICES = (
		(ADMIN, 'Admin'),
		(EMPLOYEE, 'Employee'),
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
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
	
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profiiles.save()	

	
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
	devID = models.AutoField(
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
	devID = models.ForeignKey(
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
	devID = models.ForeignKey(
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
	srcDevID = models.IntegerField(
	)
	srcDevPort = models.IntegerField(
	)
	destDevID = models.IntegerField(
	)
	destDevPort	= models.IntegerField(
	)
	cableType = models.CharField(
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
	srcDevID = models.IntegerField(
	)
	srcDevPort = models.IntegerField(
	)
	destDevID = models.IntegerField(
	)
	destDevPort = models.IntegerField(
	)
	cableType = models.CharField(
		max_length=10,
		choices=CONNECTION_TYPE_CHOICES,
	)

class SaveDev(models.Model):
	saveID = models.AutoField(
		primary_key=True
	)
	xCord = models.IntegerField(
	)
	yCord = models.IntegerField(
	)
	devID = models.IntegerField(
	)

class Logs(models.Model):
	logID = models.AutoField(
		primary_key=True
	)
	devID = models.ForeignKey(
		'Device',
		on_delete=models.CASCADE,
	)
	userID = models.ForeignKey(
		'User',
		on_delete=models.CASCADE,
	)
	timestamp = models.DateTimeField(
		auto_now_add=True, blank=True
	)
	
	
	


# Create your models here.
