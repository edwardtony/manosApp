# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 22:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apiREST', '0007_auto_20170522_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 22, 37, 33, 606079, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 22, 37, 33, 614079, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 22, 37, 33, 598080, tzinfo=utc)),
        ),
    ]
