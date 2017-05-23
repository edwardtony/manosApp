# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 22:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apiREST', '0006_auto_20170522_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='tag',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 22, 27, 45, 739168, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 22, 27, 45, 745168, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 22, 27, 45, 733168, tzinfo=utc)),
        ),
    ]
