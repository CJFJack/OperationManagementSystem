#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkcms.request.v20180308 import QueryMetricLastRequest
import json
from django.conf import settings

AccessKeyId = settings.ACCESS_KEY_ID
AccessKeySecret = settings.ACCESS_KEY_SECRET
clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')

def query_rds_monitor(instanceId, metric):
    # 设置参数
    request = QueryMetricLastRequest.QueryMetricLastRequest()
    request.set_accept_format('json')

    request.add_query_param('Project', 'acs_rds_dashboard')
    request.add_query_param('Metric', metric)
    request.add_query_param('Dimensions', {'instanceId': instanceId})
    request.add_query_param('Period', '300')

    # 发起请求
    response = clt.do_action(request)
    json_response = json.loads(response)
    try:
        average = json.loads(json_response['Datapoints'])[0]['Average']
    except:
        return 0
    else:
        return average


# 调用函数
if __name__ == '__main__':
    instance_id = "rdsmaqvrzazju6n"
    result = query_rds_monitor(instanceId=instance_id, metric="CpuUsage")
    print result
    result = query_rds_monitor(instanceId=instance_id, metric="IOPSUsage")
    print result
    result = query_rds_monitor(instanceId=instance_id, metric="DiskUsage")
    print result