# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from OperationManagementSystem.apps.system.models import Application


class DeployApply(models.Model):
    WAITFORCOMMIT = 'WC'
    WAITFORDEPLOY = 'WD'
    CANCELED = 'C'
    DEPLOYED = 'D'
    DEVMANAGERAPPROVAL = 'DA'
    OPERMANAGERAPPROVAL = 'OA'
    ENGINEERAPPROVAL = 'EA'
    TESTMANAGERAPPROVAL = 'TA'
    TECHNICALDIRECTORYAPPROVAL = 'TDA'
    status_CHOICES = (
        (WAITFORCOMMIT, '待提交'),
        (WAITFORDEPLOY, '待发布'),
        (CANCELED, '已取消'),
        (DEPLOYED, '已发布'),
        (DEVMANAGERAPPROVAL, '研发经理审批中'),
        (OPERMANAGERAPPROVAL, '运维经理审批中'),
        (ENGINEERAPPROVAL, '运维工程师审批中'),
        (TESTMANAGERAPPROVAL, '测试经理审批中'),
        (TECHNICALDIRECTORYAPPROVAL, '技术总监审批中'),
    )
    apply_name = models.CharField("申请编号", max_length=50)
    status = models.CharField(
        "申请状态",
        max_length=3,
        choices=status_CHOICES,
        default=WAITFORCOMMIT,
    )
    apply_user = models.CharField("申请人", max_length=20, null=True, blank=True)
    apply_time = models.DateTimeField("申请时间", auto_now_add=True)
    deploy_user = models.CharField("发布人", max_length=20, null=True, blank=True)
    deploy_time = models.DateTimeField("实际发布时间", null=True, blank=True)
    conf_amend_explain = models.TextField("配置修改说明", null=True, blank=True)
    remark_explain = models.TextField("备注事项", null=True, blank=True)
    verify_result = models.CharField(
        max_length=1,
        choices=(('Y', '审核通过'), ('N', '审核不通过')),
        null=True,
        blank=True,
        verbose_name="审核结果"
    )
    wish_deploy_time = models.DateField("期望发布日期", null=True, blank=True)

    class Meta:
        verbose_name = u'发布申请列表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.apply_name


class DeployApplyOperateLog(models.Model):
    deploy_apply = models.ForeignKey(DeployApply, on_delete=models.CASCADE, verbose_name=u'所属申请发布单')
    type = models.CharField(max_length=10, verbose_name=u'发布应用代码类型')
    operator_name = models.CharField(max_length=30, verbose_name=u'操作人')
    operation_time = models.DateTimeField(auto_now_add=True, verbose_name=u'操作时间')

    class Meta:
        verbose_name = u'发布申请审批日志'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.operator_name
