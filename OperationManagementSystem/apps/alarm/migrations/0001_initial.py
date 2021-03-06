# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-18 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlarmHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u544a\u8b66\u89c4\u5219\u540d\u79f0')),
                ('namespace', models.CharField(max_length=30, verbose_name='\u544a\u8b66\u4ea7\u54c1\u540d\u79f0')),
                ('alarm_time', models.DateTimeField(blank=True, null=True, verbose_name='\u544a\u8b66\u65f6\u95f4')),
                ('value', models.CharField(max_length=10, verbose_name='\u544a\u8b66\u7684\u5f53\u524d\u503c')),
                ('instance_name', models.CharField(max_length=50, verbose_name='\u544a\u8b66\u5b9e\u4f8b\u540d\u79f0')),
                ('metric_name', models.CharField(max_length=50, verbose_name='\u76d1\u63a7\u9879\u540d\u79f0')),
                ('dimension', models.CharField(max_length=200, verbose_name='\u544a\u8b66\u8be6\u60c5')),
            ],
            options={
                'verbose_name': '\u544a\u8b66\u5386\u53f2',
                'verbose_name_plural': '\u544a\u8b66\u5386\u53f2',
            },
        ),
    ]
