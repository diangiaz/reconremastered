from django.contrib import admin
from .models import Profile, Device, Port, Group, GroupToDevice, SaveTopology, SaveConn, SaveDev, Log, Comport, MainSwitchPort

admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(Port)
admin.site.register(Group)
admin.site.register(GroupToDevice)
admin.site.register(SaveTopology)
admin.site.register(SaveConn)
admin.site.register(SaveDev)
admin.site.register(Log)
admin.site.register(Comport)
admin.site.register(MainSwitchPort)
