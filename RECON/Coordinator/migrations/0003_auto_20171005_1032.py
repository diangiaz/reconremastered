# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-05 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Coordinator', '0002_auto_20171001_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='usertype',
            field=models.CharField(max_length=10),
        ),
    ]
