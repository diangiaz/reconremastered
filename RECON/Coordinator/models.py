from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


EMPLOYEE_TYPE_CHOICES = (
		('admin', 'Admin'),
		('employee', 'Employee'),
	)
	
class Group(models.Model):
	name = models.CharField(
		unique=True, max_length=50,)
		
	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	usertype = models.CharField(
		max_length=10,
	)
	employeeID = models.CharField(
		max_length=10,
	)
	group = models.ForeignKey(
		Group,
		on_delete = models.CASCADE,	
		default = 1,
	)
	
	def __str__(self):
		return "%s's profile" % self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		# print("Profile created")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
		
post_save.connect(create_user_profile, sender=User)	
	
	
	
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
	type = models.CharField(
		max_length=25,
		choices=DEVICE_TYPE_CHOICES
	)
	name = models.CharField(
		unique=True,
		max_length=25,
	)
	ycord = models.PositiveIntegerField(
	)
	xcord = models.PositiveIntegerField(
	)
	def __str__(self):
		return self.name

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
		unique=True,
		max_length=25,
	)
	type = models.CharField(
		max_length=20,
		choices=PORT_TYPE_CHOICES
	)
	device = models.ForeignKey(
		Device,
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
	group = models.ForeignKey(
		Group,
		on_delete=models.CASCADE,
	)
	device = models.ForeignKey(
		Device,
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
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	group = models.ForeignKey(
		Group,
		on_delete=models.CASCADE,
	)

class Connection(models.Model):
	CONSOLE = 'Console'
	SERIAL = 'Serial'
	STRAIGHT = 'Straight'
	CONNECTION_TYPE_CHOICES = (
		(CONSOLE, 'Console'),
		(SERIAL, 'Serial'),
		(STRAIGHT, 'Straight'),
	)
	Group = models.ForeignKey(
		Group,
		on_delete = models.CASCADE,
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

class Config(models.Model):
	group = models.ForeignKey(
		Group,
		on_delete=models.CASCADE,
	)
	device = models.ForeignKey(
		Device,
		on_delete=models.CASCADE,
	)
	config = models.FileField(
		upload_to=None,
		max_length=100,
	)

class SaveTopology(models.Model):
	group = models.ForeignKey(
		Group,
		on_delete=models.CASCADE,
	)
	name = models.CharField(
		max_length = 40
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
	xCord = models.IntegerField(
	)
	yCord = models.IntegerField(
	)
	devID = models.IntegerField(
	)

class Log(models.Model):
	device = models.ForeignKey(
		Device,
		on_delete=models.CASCADE,
	)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	timestamp = models.DateTimeField(
		auto_now_add=True, blank=True
	)
	
	
	

