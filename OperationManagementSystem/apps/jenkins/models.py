# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class JenkinsJobList(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Jenkins任务名称')
    last_success_num = models.IntegerField(default=0, verbose_name=u'最后一次成功构建版本号')

    class Meta:
        verbose_name = u'Jenkins任务列表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
