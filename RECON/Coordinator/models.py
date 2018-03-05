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
	unique=True,
	max_length=50,
	)
		
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
		null = True,
		blank = True,
	)
	
	def __str__(self):
		return "%s's profile" % self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
		
post_save.connect(create_user_profile, sender=User)	

class Comport(models.Model):
	name = models.CharField(
		max_length=10
	)
	istaken = models.CharField(
		max_length=1,
		default='0',
	)
	def __str__(self):
		return self.name

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
		max_length=25,
	)
	serialIndex = models.IntegerField(
		default=0
	)
	comport = models.ForeignKey(
		Comport,
		on_delete=models.CASCADE,
	)
	def __str__(self):
		return self.name
		
class MainSwitchPort(models.Model):
	name = models.CharField(
		max_length=6
	)
	istaken = models.CharField(
		max_length=1,
		default=0,
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
	istaken = models.CharField(
		max_length=1,
		default = '0',
	)
	isactive = models.CharField(
		max_length=1,
		default='0',
	)
	mainswitchport = models.ForeignKey(
		MainSwitchPort,
		on_delete=models.CASCADE,
		null = True,
	)
	def __str__(self):
		return self.name + " of " + self.device.name
	
class GroupToDevice(models.Model):
	RESERVE = 'RS'
	APPROVE = 'AP'
	ALLOCATION = 'AL'
	DECLINED = 'DC'
	TYPE_CHOICES = (
		(RESERVE, 'Reserve'),
		(APPROVE, 'Approve'),
		(ALLOCATION, 'Allocation'),
		(DECLINED, 'Declined'),
	)
	group = models.ForeignKey(
		Group,
		on_delete=models.CASCADE,
	)
	device = models.ForeignKey(
		Device,
		on_delete=models.CASCADE,
	)
	startDateTime = models.DateField(
		auto_now=False,
		auto_now_add=False,
		)
	endDateTime = models.DateField(
		auto_now=False,
		auto_now_add=False,
	)
	type = models.CharField(
		max_length = 2,
		choices = TYPE_CHOICES,
	)
	
	def __str__(self):
		return self.group.name + " to " + self.device.name

class Connection(models.Model):
	CONSOLE = 'Console'
	SERIAL = 'Serial'
	STRAIGHT = 'Straight'
	CONNECTION_TYPE_CHOICES = (
		(CONSOLE, 'Console'),
		(SERIAL, 'Serial'),
		(STRAIGHT, 'Straight'),
	)
	group = models.ForeignKey(
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
	def __str__(self):
		return self.name

class SaveConn(models.Model):
	saveTopology = models.ForeignKey(
		SaveTopology,
		on_delete=models.CASCADE,
	)
	connectionName = models.CharField(
		max_length=25,
	)
	srcDevice = models.CharField(
		max_length=25,
	)
	srcPort = models.CharField(
		max_length=25,
	)
	endDevice = models.CharField(
		max_length=25,
	)
	endPort = models.CharField(
		max_length=25,
	)
	cableType = models.CharField(
		max_length=25,
	)
	startX = models.FloatField(
		default = 0,
	)
	startY = models.FloatField(
		default = 0,
	)
	endX = models.FloatField(
		default = 0,
	)
	endY = models.FloatField(
		default = 0,
	)
	def __str__(self):
		return self.connectionName + " between " + self.srcDevice + " and " + self.endDevice + " of " + self.saveTopology.name

class SaveDev(models.Model):
	saveTopology = models.ForeignKey(
		SaveTopology,
		on_delete=models.CASCADE,
	)
	GroupToDevice = models.ForeignKey(
		GroupToDevice,
		on_delete=models.CASCADE,
	)
	deviceName = models.CharField(
		max_length = 40,
	)
	xCord = models.FloatField(
		default = 0,
		null = True,
	)
	yCord = models.FloatField(
		default = 0,
		null = True,
	)
	def __str__(self):
		return self.deviceName + " of " + self.saveTopology.name

class Log(models.Model):
	device = models.ForeignKey(
		Device,
		on_delete=models.CASCADE
	)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	timestamp = models.DateTimeField(
		auto_now_add=True, 
		blank=True,
	)
	action = models.CharField(
		max_length = 50,
	)
	def __str__(self):
		return self.user.username + "(" + str(self.timestamp) + "): " + self.action
	
	
	

