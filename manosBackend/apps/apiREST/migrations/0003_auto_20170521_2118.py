# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 02:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apiREST', '0002_auto_20170521_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2017, 5, 22, 2, 18, 9, 443719, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='pub_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2017, 5, 22, 2, 18, 9, 453716, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2017, 5, 22, 2, 18, 9, 418718, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'A'), ('INACTIVE', 'I')], default='A', max_length=2),
        ),
    ]
