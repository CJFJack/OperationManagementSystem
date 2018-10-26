#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import json
from django.conf import settings

AccessKeyId = settings.ACCESS_KEY_ID
AccessKeySecret = settings.ACCESS_KEY_SECRET
client = AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')


def acs_alarm_history(starttime, endtime):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('metrics.cn-hangzhou.aliyuncs.com')
    request.set_method('POST')
    request.set_version('2018-03-08')
    request.set_action_name('ListAlarmHistory')

    request.add_query_param('StartTime', starttime)
    request.add_query_param('EndTime', endtime)

    response = client.do_action_with_exception(request)
    json_response = json.loads(response)
    alarm_history_list = json_response['AlarmHistoryList']
    alarm_history = alarm_history_list['AlarmHistory']
    return alarm_history


if __name__ == '__main__':
    result = acs_alarm_history(starttime='2018-08-01 00:00:00', endtime='2018-08-08 00:00:00')
    print result
    n = 0
    for h in result:
        if h['Status'] == 0:
            n = n + 1
            print h['Name']
            print h['Namespace']
            print h['AlarmTime']
            print h['Value']
            print h['InstanceName']
            print h['MetricName']
            print h['Dimension']
    print (n)
