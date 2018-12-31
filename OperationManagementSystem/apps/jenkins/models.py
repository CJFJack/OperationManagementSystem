# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class JenkinsJobList(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'Jenkins任务名称')
    status = models.IntegerField(choices=((1, '运行中'), (2, '空闲')), default=2, verbose_name=u'任务当前状态')

    class Meta:
        verbose_name = u'Jenkins任务列表'
        verbose_name_plural = verbose_name

    def get_last_build_result(self):
        if self.jenkinsbuildhistory_set.all():
            return self.jenkinsbuildhistory_set.order_by('-id')[0].get_result_display()
        else:
            return ''

    def get_last_success_build_time(self):
        if self.jenkinsbuildhistory_set.filter(result=1):
            return self.jenkinsbuildhistory_set.filter(result=1).order_by('-id')[0].build_finish_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ''

    def get_last_failure_build_time(self):
        if self.jenkinsbuildhistory_set.filter(result=0):
            return self.jenkinsbuildhistory_set.filter(result=0).order_by('-id')[0].build_finish_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ''

    def __unicode__(self):
        return self.name


class JenkinsBuildHistory(models.Model):
    job = models.ForeignKey(JenkinsJobList, on_delete=models.CASCADE, verbose_name=u'所属jenkins任务')
    build_no = models.IntegerField(default=1, verbose_name=u'构建版本号')
    build_start_time = models.DateTimeField(verbose_name=u'构建开始时间')
    build_finish_time = models.DateTimeField(auto_now_add=True, verbose_name=u'构建完成时间')
    result = models.IntegerField(choices=((1, '成功'), (0, '失败')), default=1, verbose_name=u'构建结果')
    console = models.TextField(null=True, blank=True, verbose_name=u'console输出日志')

    class Meta:
        verbose_name = u'jenkins构建历史记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.job.name + '-' + self.get_result_display()
