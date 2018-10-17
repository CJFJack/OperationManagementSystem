# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class ECS(models.Model):
    ENABLE = 'Y'
    DISABLE = 'N'
    status_CHOICES = (
        (ENABLE, 'enable'),
        (DISABLE, 'disable'),
    )
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'ECS名称')
    instance_id = models.CharField(max_length=30, verbose_name=u'实例ID')
    IP = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True, verbose_name=u'IP地址')
    status = models.CharField(
        max_length=1,
        choices=status_CHOICES,
        default=ENABLE,
    )
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    recently_cpu = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name=u'最近CPU使用率')
    recently_memory = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                          verbose_name=u'最近内存使用率')
    recently_disk_usage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                              verbose_name=u'最近磁盘使用率')
    regionId = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'所在区域')
    expired_time = models.DateTimeField(null=True, blank=True, verbose_name=u'过期时间')
    memory = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'内存大小')
    os_type = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'操作系统类型')
    instance_status = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'实例状态')
    network_type = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'网络类型')
    cpu = models.CharField(max_length=5, null=True, blank=True, verbose_name=u'CPU核数')
    public_ip_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True, verbose_name=u'公网IP')
    osname = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'操作系统名称')

    class Meta:
        verbose_name = u'ECS信息表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class ApplicationRace(models.Model):
    race_id = models.BigIntegerField()
    alias = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = u'应用族群信息表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.alias)


class Application(models.Model):
    ENABLE = 'Y'
    DISABLE = 'N'
    status_CHOICES = (
        (ENABLE, 'enable'),
        (DISABLE, 'disable'),
    )
    fullname = models.CharField(max_length=50, verbose_name=u'应用全称')
    short_name = models.CharField(null=True, blank=True, max_length=30, verbose_name=u'应用简称')
    config_dir_name = models.CharField(null=True, blank=True, max_length=50, verbose_name=u'配置文件夹名称')
    ECS_lists = models.ManyToManyField(ECS, verbose_name=u'关联ECS列表')
    port = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=u'应用端口')
    test_page = models.CharField(null=True, blank=True, max_length=30, verbose_name=u'测试页面')
    dev_charge = models.CharField(null=True, blank=True, max_length=10, verbose_name=u'研发负责人')
    deploy_attention = models.TextField(null=True, blank=True, verbose_name=u'发布注意事项')
    modified_time = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')
    modified_user = models.CharField(max_length=20, default='admin', verbose_name=u'修改人')
    status = models.CharField(
        null=True, blank=True,
        max_length=1,
        choices=status_CHOICES,
        default=ENABLE,
        verbose_name=u'状态'
    )
    application_race = models.ForeignKey(ApplicationRace, on_delete=models.CASCADE, null=True, blank=True,
                                         verbose_name=u'关联站点族')
    random_id = models.IntegerField(verbose_name=u'应用随机ID')

    class Meta:
        verbose_name = u'应用信息表'

    def __unicode__(self):
        return self.fullname


class SLB(models.Model):
    instance_id = models.CharField(max_length=50, verbose_name=u'实例ID')
    name = models.CharField(max_length=30, verbose_name=u'实例名称')
    status = models.CharField(max_length=30, verbose_name=u'实例状态')
    ip = models.GenericIPAddressField(protocol='IPv4', verbose_name=u'IP地址')
    network_type = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'网络类型')
    address_type = models.CharField(max_length=10, verbose_name=u'IP类型类型')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'负载均衡信息表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class RDS(models.Model):
    instance_id = models.CharField(max_length=100, verbose_name=u'实例ID')
    instance_alias = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'实例别名')
    network_type = models.CharField(max_length=20, verbose_name=u'网络类型')
    engine = models.CharField(max_length=30, verbose_name=u'引擎类型')
    engine_version = models.CharField(max_length=50, verbose_name=u'引擎版本')
    status = models.CharField(max_length=30, verbose_name=u'状态')
    expire_time = models.DateTimeField(verbose_name=u'过期时间')

    class Meta:
        verbose_name = u'RDS信息表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.instance_id


class RDSUsageRecord(models.Model):
    rds = models.ForeignKey(RDS, on_delete=models.CASCADE, verbose_name=u'所属RDS')
    cpu_usage = models.FloatField(null=True, blank=True, verbose_name=u'CPU使用率')
    io_usage = models.FloatField(null=True, blank=True, verbose_name=u'IOPS使用率')
    disk_usage = models.FloatField(null=True, blank=True, verbose_name=u'磁盘使用率')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'RDS资源使用率记录表'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.add_time)
