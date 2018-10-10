# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class AlarmHistory(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'告警规则名称')
    namespace = models.CharField(max_length=30, verbose_name=u'告警产品名称')
    alarm_time = models.DateTimeField(null=True, blank=True, verbose_name=u'告警时间')
    value = models.CharField(max_length=10, verbose_name=u'告警的当前值')
    instance_name = models.CharField(max_length=50, verbose_name=u'告警实例名称')
    metric_name = models.CharField(max_length=50, verbose_name=u'监控项名称')
    dimension = models.CharField(max_length=200, verbose_name=u'告警详情')

    class Meta:
        verbose_name = u'告警历史'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
