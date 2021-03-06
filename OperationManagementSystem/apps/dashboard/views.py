# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from OperationManagementSystem.apps.alarm.models import AlarmHistory
from OperationManagementSystem.apps.system.models import RDSUsageRecord
from django.http import HttpResponse
from django.db.models import Count, Avg
import datetime
import json

app_name = 'dashboard'


@login_required(login_url='/login/')
def alarm_charts(request):
    return render(request, 'dashboard/alarm.html', {})


@login_required(login_url='/login/')
def index_alarm_product_type_pie(request):
    # 按alarm产品类型统计（默认为最近30天）
    now = datetime.datetime.now()
    ever = now - datetime.timedelta(days=30)
    alarm = AlarmHistory.objects.filter(alarm_time__gt=ever).values('namespace').annotate(Count("id"))
    product_type_list = []
    for i in alarm:
        product_type_list.append(str(i['namespace']))
    product_type_alarm_list = []
    for i in alarm:
        product_type_dict = {str('value'): i['id__count'], str('name'): str(i['namespace'])}
        product_type_alarm_list.append(product_type_dict)
    return HttpResponse(json.dumps({'success': True, 'product_type_list': product_type_list,
                                    'product_type_alarm_list': product_type_alarm_list}),
                        content_type="application/json")


@login_required(login_url='/login/')
def index_alarm_metric_type_pie(request):
    # 按alarm监控项类型统计（默认为最近30天）
    now = datetime.datetime.now()
    ever = now - datetime.timedelta(days=30)
    alarm = AlarmHistory.objects.filter(alarm_time__gt=ever).values('metric_name').annotate(Count("id"))
    metric_type_list = []
    for i in alarm:
        metric_type_list.append(str(i['metric_name']))
    metric_type_alarm_list = []
    for i in alarm:
        metric_type_dict = {str('value'): i['id__count'], str('name'): str(i['metric_name'])}
        metric_type_alarm_list.append(metric_type_dict)
    return HttpResponse(json.dumps({'success': True, 'metric_type_list': metric_type_list,
                                    'metric_type_alarm_list': metric_type_alarm_list}),
                        content_type="application/json")


@login_required(login_url='/login/')
def index_alarm_instance_pie(request):
    # 按alarm实例比例统计（默认为最近30天）
    now = datetime.datetime.now()
    ever = now - datetime.timedelta(days=30)
    alarm = AlarmHistory.objects.filter(alarm_time__gt=ever).values('instance_name').annotate(Count("id"))
    instance_list = []
    for i in alarm:
        instance_list.append(i['instance_name'])
    instance_alarm_list = []
    for i in alarm:
        instance_dict = {'value': i['id__count'], 'name': i['instance_name']}
        instance_alarm_list.append(instance_dict)
    return HttpResponse(json.dumps({'success': True, 'instance_list': instance_list,
                                    'instance_alarm_list': instance_alarm_list}),
                        content_type="application/json")


@login_required(login_url='/login/')
def index_alarm_line(request):
    start = str(datetime.datetime.now())[:4] + '-01-01'
    end = str(datetime.datetime.now())[:4] + '-12-31'
    alarm = AlarmHistory.objects.filter(alarm_time__gt=start).filter(alarm_time__lt=end). \
        extra(select={'month': 'month(alarm_time)'}).values('month').annotate(number=Count('id'))
    alarm_num_x = []
    alarm_num_y = []
    this_year = str(datetime.datetime.now())[:4]
    for m in xrange(1, 13):
        this_date = this_year + '-' + str(m)
        alarm_num_x.append(this_date)
    for m in xrange(1, 13):
        try:
            dict_index = [int(a['month']) for a in alarm].index(m)
        except Exception, e:
            alarm_num_y.append(0)
            print e
        else:
            alarm_num_y.append([a for a in alarm][dict_index]['number'])
    return HttpResponse(json.dumps({'success': True, 'alarm_num_x': alarm_num_x, 'alarm_num_y': alarm_num_y}),
                        content_type="application/json")


@login_required(login_url='/login/')
def rds_charts(request):
    return render(request, 'dashboard/rds.html', {})


@login_required(login_url='/login/')
def index_rds_cpu_pie(request):
    # 获取最近一次rds资源
    last_rds_resource = RDSUsageRecord.objects.order_by('-add_time')[:1]
    # 获取最近一次rds资源cpu使用率
    try:
        last_rds_cpu = [q.cpu_usage for q in last_rds_resource][0]
    except:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': True, 'last_rds_cpu': last_rds_cpu}),
                            content_type="application/json")


@login_required(login_url='/login/')
def index_rds_io_pie(request):
    # 获取最近一次rds资源
    last_rds_resource = RDSUsageRecord.objects.order_by('-add_time')[:1]
    # 获取最近一次rds资源IO使用率
    try:
        last_rds_io = [q.io_usage for q in last_rds_resource][0]
    except:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': True, 'last_rds_io': last_rds_io}), content_type="application/json")


@login_required(login_url='/login/')
def index_rds_disk_pie(request):
    # 获取最近一次rds资源
    last_rds_resource = RDSUsageRecord.objects.order_by('-add_time')[:1]
    # 获取最近一次rds资源IO使用率
    try:
        last_rds_disk = [q.disk_usage for q in last_rds_resource][0]
    except:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': True, 'last_rds_disk': last_rds_disk}),
                            content_type="application/json")


@login_required(login_url='/login/')
def index_rds_line(request):
    # 默认横坐标间隔
    select_count = 12
    select_range = request.POST['select_range']
    if select_range == u'1小时':
        select_count = 12
    if select_range == u'6小时':
        select_count = 72
    if select_range == u'12小时':
        select_count = 144
    if select_range == u'1天':
        select_count = 288
    if select_range == u'3天':
        select_count = 864
    if select_range == u'7天':
        select_count = 2016
    if select_range == u'14天':
        select_count = 4032
    try:
        # 获取最近12次rds资源, 默认5分钟为间隔
        recently_rds_resource = RDSUsageRecord.objects.order_by('-add_time')[:select_count]
        # 获取最近12次add_time的list
        add_time_list = [q.add_time.strftime('%Y-%m-%d %H:%M') for q in recently_rds_resource]
        add_time_list.sort()
        add_time = add_time_list
        # 获取最近12次rds的CPU使用率list
        recently_rds_cpu = [q.cpu_usage for q in recently_rds_resource]
        recently_rds_cpu.reverse()
        # 获取最近12次rds的I/O使用率list
        recently_rds_io = [q.io_usage for q in recently_rds_resource]
        recently_rds_io.reverse()
        # 获取最近12次rds的disk使用率list
        recently_rds_disk = [q.disk_usage for q in recently_rds_resource]
        recently_rds_disk.reverse()
    except:
        return HttpResponse(json.dumps({'success': False}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'success': True, 'add_time': add_time,
                                        'recently_rds_cpu': recently_rds_cpu, 'recently_rds_io': recently_rds_io,
                                        'recently_rds_disk': recently_rds_disk}), content_type="application/json")
