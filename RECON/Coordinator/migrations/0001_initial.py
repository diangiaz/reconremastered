# Generated by Django 2.0.1 on 2018-03-05 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('istaken', models.CharField(default='0', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.FileField(upload_to=None)),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('srcDevID', models.IntegerField()),
                ('srcDevPort', models.IntegerField()),
                ('destDevID', models.IntegerField()),
                ('destDevPort', models.IntegerField()),
                ('cableType', models.CharField(choices=[('Console', 'Console'), ('Serial', 'Serial'), ('Straight', 'Straight')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Router', 'Router'), ('Switch', 'Switch'), ('Terminal', 'Terminal'), ('Server', 'Server')], max_length=25)),
                ('name', models.CharField(max_length=25)),
                ('serialIndex', models.IntegerField(default=0)),
                ('comport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Comport')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupToDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDateTime', models.DateField()),
                ('endDateTime', models.DateField()),
                ('type', models.CharField(choices=[('RS', 'Reserve'), ('AP', 'Approve'), ('AL', 'Allocation'), ('DC', 'Declined')], max_length=2)),
                ('adminNotifStatus', models.CharField(choices=[('SE', 'SE'), ('US', 'US')], default='US', max_length=2, null=True)),
                ('admintimestamp', models.DateTimeField(auto_now_add=True)),
                ('userNotifStatus', models.CharField(choices=[('SE', 'SE'), ('US', 'US')], default='SE', max_length=2, null=True)),
                ('usertimestamp', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Device')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=50)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Device')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MainSwitchPort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=6)),
                ('istaken', models.CharField(default=0, max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('type', models.CharField(choices=[('Serial', 'Serial'), ('Gigabyte', 'Gigabyte'), ('Fast Ethernet', 'Fast Ethernet'), ('Console', 'Console')], max_length=20)),
                ('istaken', models.CharField(default='0', max_length=1)),
                ('isactive', models.CharField(default='0', max_length=1)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Device')),
                ('mainswitchport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Coordinator.MainSwitchPort')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertype', models.CharField(max_length=10)),
                ('employeeID', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Disable', 'Disable')], default='Active', max_length=7)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SaveConn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connectionName', models.CharField(max_length=25)),
                ('srcDevice', models.CharField(max_length=25)),
                ('srcPort', models.CharField(max_length=25)),
                ('endDevice', models.CharField(max_length=25)),
                ('endPort', models.CharField(max_length=25)),
                ('cableType', models.CharField(max_length=25)),
                ('startX', models.FloatField(default=0)),
                ('startY', models.FloatField(default=0)),
                ('endX', models.FloatField(default=0)),
                ('endY', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SaveDev',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceName', models.CharField(max_length=40)),
                ('xCord', models.FloatField(default=0, null=True)),
                ('yCord', models.FloatField(default=0, null=True)),
                ('GroupToDevice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.GroupToDevice')),
            ],
        ),
        migrations.CreateModel(
            name='SaveTopology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Group')),
            ],
        ),
        migrations.AddField(
            model_name='savedev',
            name='saveTopology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.SaveTopology'),
        ),
        migrations.AddField(
            model_name='saveconn',
            name='saveTopology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.SaveTopology'),
        ),
        migrations.AddField(
            model_name='connection',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Group'),
        ),
        migrations.AddField(
            model_name='config',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Device'),
        ),
        migrations.AddField(
            model_name='config',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Group'),
        ),
    ]
