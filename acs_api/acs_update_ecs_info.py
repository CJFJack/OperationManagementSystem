#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import json
from django.conf import settings

AccessKeyId = settings.ACCESS_KEY_ID
AccessKeySecret = settings.ACCESS_KEY_SECRET
clt = client.AcsClient(AccessKeyId, AccessKeySecret, 'cn-hangzhou')


def update_ecs_info(instance_id):
    # 设置参数
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')
    request.add_query_param('RegionId', 'cn-hangzhou')
    request.add_query_param('InstanceIds', instance_id)

    # 发起请求
    response = clt.do_action(request)
    json_response = json.loads(response)
    
    # 获取实例区域
    region_id = json_response['Instances']['Instance'][0]['RegionId']
    # 获取过期时间
    expire_time = json_response['Instances']['Instance'][0]['ExpiredTime']
    # 获取内存大小
    memory = json_response['Instances']['Instance'][0]['Memory']
    # 获取系统类型
    os_type = json_response['Instances']['Instance'][0]['OSType']
    # 获取实例状态
    status = json_response['Instances']['Instance'][0]['Status']
    # 获取网络类型
    network_type = json_response['Instances']['Instance'][0]['InstanceNetworkType']
    # 获取内网IP
    inner_ip_address = json_response['Instances']['Instance'][0]['InnerIpAddress']['IpAddress'][0]
    # 获取实例名称
    instance_name = json_response['Instances']['Instance'][0]['InstanceName']
    # 获取CPU核数
    cpu = json_response['Instances']['Instance'][0]['Cpu']
    # 获取公网IP
    try:
        public_ip_address = json_response['Instances']['Instance'][0]['PublicIpAddress']['IpAddress'][0]
    except:
        public_ip_address = ''
    # 获取操作系统版本
    os_name = json_response['Instances']['Instance'][0]['OSName']

    # 存入字典
    dict = {}
    dict['RegionId'] = region_id
    dict['ExpiredTime'] = expire_time.replace("Z", "").replace("T", " ")
    dict['Memory'] = memory
    dict['OSType'] = os_type
    dict['Status'] = status
    dict['NetworkType'] = network_type
    dict['InnerIpAddress'] = inner_ip_address
    dict['InstanceName'] = instance_name
    dict['Cpu'] = cpu
    dict['PublicIpAddress'] = public_ip_address
    dict['OSName'] = os_name
    
    return dict
    
    
# 调用函数
if __name__ == '__main__':
    result = update_ecs_info(instance_id=["AY140507114807874a62"])
    print (result)
