from django.contrib import admin
from .models import Profile, Device, Group, Port, GroupToDevice, UserToGroup, Connection, Config, SaveTopology, SaveConn, SaveDev, Log

admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(Group)
admin.site.register(Port)
admin.site.register(GroupToDevice)
admin.site.register(UserToGroup)
admin.site.register(Connection)
admin.site.register(Config)
admin.site.register(SaveTopology)
admin.site.register(SaveConn)
admin.site.register(SaveDev)
admin.site.register(Log)
