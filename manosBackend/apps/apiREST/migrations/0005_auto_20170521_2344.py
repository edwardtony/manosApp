# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 04:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apiREST', '0004_auto_20170521_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 4, 44, 13, 670786, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='status',
            field=models.CharField(choices=[('CHOSEN', 'C'), ('WAITING', 'W')], default='W', max_length=10),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 4, 44, 13, 676802, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='status',
            field=models.CharField(choices=[('CREATED', 'C'), ('QUOTED', 'Q'), ('FINISHED', 'F')], default='C', max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 22, 4, 44, 13, 662783, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='worker',
            name='status',
            field=models.CharField(choices=[('VALIDATED', 'V'), ('UNVALIDATED', 'U')], default='U', max_length=10),
        ),
    ]
