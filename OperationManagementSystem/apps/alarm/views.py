# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .models import AlarmHistory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count, Avg
import datetime
import json


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
        product_type_dict = {}
        product_type_dict[str('value')] = i['id__count']
        product_type_dict[str('name')] = str(i['namespace'])
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
