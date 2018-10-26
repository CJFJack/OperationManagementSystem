#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
import json, time
from django.conf import settings

AccessKeyId = settings.ACCESS_KEY_ID
AccessKeySecret = settings.ACCESS_KEY_SECRET
clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')

def query_rds_list(RegionId):
    # 设置参数
    request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    request.set_accept_format('json')
    request.add_query_param('RegionId', RegionId)

    # 发起请求
    response = clt.do_action(request)
    json_response = json.loads(response)
    return json_response['Items']['DBInstance'][0]


# 调用函数
if __name__ == '__main__':
    result = query_rds_list(RegionId="cn-hangzhou")
    print 'DBInstanceId = ' + result['DBInstanceId']
    print 'network_type = ' + result['InstanceNetworkType']
    print 'engine = ' + result['Engine']
    print 'engine_version = ' + result['EngineVersion']
    print 'status = ' + result['DBInstanceStatus']
    print 'expire_time = ' + result['ExpireTime'].replace("Z", "").replace("T", " ")
