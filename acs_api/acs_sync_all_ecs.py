#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import json
from django.conf import settings

AccessKeyId = settings.ACCESS_KEY_ID
AccessKeySecret = settings.ACCESS_KEY_SECRET
clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')


def sync_all_ecs(region_id):
    # 设置参数
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')
    
    request.add_query_param('RegionId', region_id)
    request.add_query_param('PageSize', 100)
    
    # 发起请求
    response = clt.do_action(request)
    
    data = json.loads(response)
    instances = data['Instances']['Instance']
    L = []
    for instance in instances:
        L.append(instance['InstanceId'])
    return L


if __name__ == '__main__':
    result = sync_all_ecs(region_id='cn-hangzhou')
    print (result)

