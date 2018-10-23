# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from simple_history.models import HistoricalRecords
from OperationManagementSystem.apps.system.models import Application


class Configfile(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, blank=True, null=True, verbose_name=u'所属应用')
    filename = models.CharField(max_length=30, verbose_name=u'配置文件名称')
    content = models.TextField(null=True, blank=True, verbose_name=u'配置内容')
    modified_user = models.CharField(max_length=20, verbose_name=u'修改人')
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    history = HistoricalRecords(verbose_name=u'修改历史记录')

    def get_application_race_application_list(self):
        return [application for application in Application.objects.all()
                if application.application_race_id == self.application.application_race_id]

    class Meta:
        verbose_name = u'配置文件信息表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.filename


class AuthUser(models.Model):
    user_id = models.IntegerField(blank=True, null=True, verbose_name=u'用户id')

    class Meta:
        verbose_name = u'模拟用户表给ConfigChangeHistory表用'
        verbose_name_plural = verbose_name


class ConfigChangeHistory(models.Model):
    id = models.IntegerField()
    filename = models.CharField(max_length=30)
    content = models.TextField(blank=True, null=True)
    modified_user = models.CharField(max_length=20)
    modified_time = models.DateTimeField()
    history_id = models.AutoField(primary_key=True)
    history_date = models.DateTimeField()
    history_change_reason = models.CharField(max_length=100, blank=True, null=True)
    history_type = models.CharField(max_length=1)
    history_user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    site_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deploy_historicalconfigfile'
        verbose_name = u'配置修改历史记录表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.filename
