# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-13 23:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booklos', '0011_auto_20160611_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='check_status',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
