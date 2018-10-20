# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from OperationManagementSystem.apps.system.models import Application, ECS, SLB
from OperationManagementSystem.apps.deploy.models import DeployApply


class Release(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name=u'所属发布应用')
    ECS = models.ForeignKey(ECS, on_delete=models.CASCADE, verbose_name=u'所属发布ECS')
    HAVEDEPLOY = 'Y'
    WAITDEPLOY = 'N'
    status_CHOICES = (
        (HAVEDEPLOY, '已发布'),
        (WAITDEPLOY, '待发布'),
    )
    status = models.CharField(
        "配置发布状态",
        max_length=1,
        choices=status_CHOICES,
        default=WAITDEPLOY,
    )
    modified_user = models.CharField(max_length=20, verbose_name=u'修改人')
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')

    class Meta:
        verbose_name = u'配置发布状态'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.status


class DeployItem(models.Model):
    TRUNK = 'T'
    BRANCH = 'B'
    type_CHOICES = (
        (TRUNK, '主干'),
        (BRANCH, '分支'),
    )
    deploy_apply = models.ForeignKey(DeployApply, on_delete=models.CASCADE, verbose_name=u'所属发布申请单')
    deploy_order_by = models.PositiveSmallIntegerField("发布顺序", null=True, blank=True)
    jenkins_version = models.PositiveSmallIntegerField("jenkins版本号", null=True, blank=True)
    type = models.CharField(
        "代码类型",
        max_length=1,
        choices=type_CHOICES,
        default=TRUNK,
    )
    deploy_application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True,
                                           verbose_name="发布应用")

    class Meta:
        verbose_name = u'发布项目列表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.deploy_application


class DeployECS(models.Model):
    deploy_apply = models.ForeignKey(DeployApply, on_delete=models.CASCADE, verbose_name=u'所属发布申请单')
    ECS = models.ForeignKey(ECS, on_delete=models.CASCADE, verbose_name=u'发布应用所属ECS')
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    ECS_deploy_status = models.CharField(max_length=1, default='N', verbose_name=u'ECS发布状态')

    class Meta:
        verbose_name = u'发布应用与ECS关联关系表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.ECS.name


class SLBToApplication(models.Model):
    SLB = models.ForeignKey(SLB, on_delete=models.CASCADE, verbose_name=u'所属SLB')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name=u'所属应用')

    class Meta:
        verbose_name = u'SLB与应用关系表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.application.fullname


class SLBHealthStatus(models.Model):
    SLB = models.ForeignKey(SLB, on_delete=models.CASCADE, verbose_name=u'所属SLB')
    ECS = models.ForeignKey(ECS, on_delete=models.CASCADE, verbose_name=u'所属ECS')
    SLBStatus = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'SLB启用状态')
    health_status = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'SLB后端应用健康状态')

    def __unicode__(self):
        return self.health_status
