#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import DescribeHealthStatusRequest
import json
from django.conf import settings

AccessKeyId = settings.ACCESS_KEY_ID
AccessKeySecret = settings.ACCESS_KEY_SECRET
clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')


def update_slb_health(LoadBalancerId):
    # 设置参数
    request = DescribeHealthStatusRequest.DescribeHealthStatusRequest()
    request.set_accept_format('json')
    
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('LoadBalancerId', LoadBalancerId)
    
    # 发起请求
    response = clt.do_action(request)
    if 'Message' in response:
        return json.loads(response)
    else:
        try:
            json.loads(response)['BackendServers']
        except:
            return {'success', 'False'}
        else:
            BackendServers = json.loads(response)['BackendServers']
            BackendServer = BackendServers['BackendServer']
            return BackendServer


if __name__ == '__main__':
    result = update_slb_health(LoadBalancerId='155a56d1c0a-cn-hangzhou-dg-a011')
    print result



