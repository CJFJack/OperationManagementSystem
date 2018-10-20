#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
import json
from django.conf import settings

AccessKeyId = settings.ACCESS_KEY_ID
AccessKeySecret = settings.ACCESS_KEY_SECRET
clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')


def sync_all_slb(region_id):
    # 设置参数
    request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
    request.set_accept_format('json')
    
    request.add_query_param('RegionId', region_id)
    
    # 发起请求
    response = clt.do_action(request)
    LoadBalancers = json.loads(response)['LoadBalancers'] 
    LoadBalancer = LoadBalancers['LoadBalancer']
    slblist = []
    for slb in LoadBalancer:
        LoadBalancerId = slb['LoadBalancerId']
        try:
            LoadBalancerName = slb['LoadBalancerName']
        except:
            LoadBalancerName = ''
        try:
            NetworkType = slb['NetworkType']
        except:
            NetworkType = ''
        LoadBalancerStatus = slb['LoadBalancerStatus']
        Address = slb['Address']
        AddressType = slb['AddressType']
        CreateTime = slb['CreateTime'].replace("Z", "").replace("T", " ")
        slbdict={}
        slbdict['LoadBalancerId'] = LoadBalancerId
        slbdict['LoadBalancerName'] = LoadBalancerName
        slbdict['LoadBalancerStatus'] = LoadBalancerStatus
        slbdict['Address'] = Address
        slbdict['AddressType'] = AddressType
        slbdict['CreateTime'] = CreateTime
        slbdict['NetworkType'] = NetworkType
        slblist.append(slbdict)
    return slblist


if __name__ == '__main__':
    slbinfo = sync_all_slb(region_id='cn-hangzhou')
    print slbinfo

