# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-17 14:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_application_application_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='application_id',
            new_name='random_id',
        ),
    ]
