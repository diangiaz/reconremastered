# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-14 16:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Coordinator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='xcord',
        ),
        migrations.RemoveField(
            model_name='device',
            name='ycord',
        ),
    ]
