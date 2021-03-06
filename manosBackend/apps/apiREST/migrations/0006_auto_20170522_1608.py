# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 21:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apiREST', '0005_auto_20170521_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 21, 8, 0, 711531, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiREST.Address'),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 21, 8, 0, 718041, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 21, 8, 0, 700012, tzinfo=utc)),
        ),
    ]
