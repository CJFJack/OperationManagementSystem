# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-17 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_auto_20181017_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='config_dir_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u914d\u7f6e\u6587\u4ef6\u5939\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='application',
            name='short_name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='\u5e94\u7528\u7b80\u79f0'),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(blank=True, choices=[('Y', 'enable'), ('N', 'disable')], default='Y', max_length=1, null=True, verbose_name='\u72b6\u6001'),
        ),
        migrations.AlterField(
            model_name='application',
            name='test_page',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='\u6d4b\u8bd5\u9875\u9762'),
        ),
    ]