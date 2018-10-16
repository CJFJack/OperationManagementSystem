#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkcms.request.v20180308 import QueryMetricLastRequest
from datetime import datetime, timedelta
import json
from django.conf import settings

AccessKeyId = settings.ACCESS_KEY_ID
AccessKeySecret = settings.ACCESS_KEY_SECRET
clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')

now = datetime.now()
start_time = str(now+timedelta(minutes=-5))
end_time = str(now)


def update_ecs_monitor(instance_id, metric):
    # 设置参数
    request = QueryMetricLastRequest.QueryMetricLastRequest()
    request.set_accept_format('json')
    request.add_query_param('Project', 'acs_ecs_dashboard')
    request.add_query_param('Metric', metric)
    request.add_query_param('Period', '60')
    request.add_query_param('Dimensions', {'instanceId': instance_id})
    request.add_query_param('StartTime', start_time)
    request.add_query_param('EndTime', end_time)
    # 发起请求
    response = clt.do_action(request)
    # json转dict
    ecs_dict=json.loads(response)
    # print ecs_dict
    # print ecs_dict['Datapoints']
    data = ecs_dict['Datapoints'].encode('utf-8')
    ecs_info = json.loads(data)[0]
    return ecs_info


# 调用函数
if __name__ == '__main__':
    result = update_ecs_monitor(instance_id="i-bp11iujuip9pks1n1ue4", metric="memory_usedutilization")
    print (result)


