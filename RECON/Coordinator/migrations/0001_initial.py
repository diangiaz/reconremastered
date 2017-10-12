# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-12 08:47
from __future__ import unicode_literals

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
                ('name', models.CharField(max_length=25, unique=True)),
                ('ycord', models.PositiveIntegerField()),
                ('xcord', models.PositiveIntegerField()),
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
                ('startDateTime', models.DateTimeField()),
                ('endDateTime', models.DateTimeField()),
                ('type', models.CharField(choices=[('RS', 'Reserve'), ('AP', 'Approve'), ('AL', 'Allocation')], max_length=2)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Device')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
                ('type', models.CharField(choices=[('Serial', 'Serial'), ('Gigabyte', 'Gigabyte'), ('Fast Ethernet', 'Fast Ethernet'), ('Console', 'Console')], max_length=20)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Device')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertype', models.CharField(max_length=10)),
                ('userID', models.CharField(default=0, max_length=10, unique=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SaveConn',
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
            name='SaveDev',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xCord', models.IntegerField()),
                ('yCord', models.IntegerField()),
                ('devID', models.IntegerField()),
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
        migrations.CreateModel(
            name='UserToGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Coordinator.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='connection',
            name='Group',
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
