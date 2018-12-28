# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ConfigFileReceiveRecord(models.Model):
    received_time = models.DateTimeField(auto_now_add=True, verbose_name=u'接收时间')
    filename = models.CharField(max_length=30, verbose_name=u'配置文件名称')
    application = models.CharField(max_length=30, verbose_name=u'所属应用')
    ECS = models.CharField(max_length=30, verbose_name=u'所属ECS服务器')

    class Meta:
        verbose_name = u'配置文件接收记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.received_time) + self.ECS + self.application + self.filename

