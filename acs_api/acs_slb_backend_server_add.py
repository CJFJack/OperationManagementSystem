#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import AddBackendServersRequest
from django.conf import settings

AccessKeyId = settings.ACCESS_KEY_ID
AccessKeySecret = settings.ACCESS_KEY_SECRET
clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')


def add_backend_server(LoadBalancerId, BackendServers):
    # 设置参数
    request = AddBackendServersRequest.AddBackendServersRequest()
    request.set_accept_format('json')
    
    request.add_query_param('LoadBalancerId', LoadBalancerId)
    request.add_query_param('BackendServers', BackendServers)
    
    # 发起请求
    response = clt.do_action(request)
    
    return response


if __name__ == '__main__':
    LoadBalancerId = '155a56d1c0a-cn-hangzhou-dg-a01'
    BackendServers = '[{"ServerId":"AY1407121019172066ee","Weight":"100"}]'
    result = add_backend_server(LoadBalancerId=LoadBalancerId, BackendServers=BackendServers)
    print (result)
