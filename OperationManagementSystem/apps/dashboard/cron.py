# -*- coding: utf-8 -*-

from acs_api import acs_alarm_history
from acs_api import acs_rds_info
from acs_api import acs_rds_monitor
from OperationManagementSystem.apps.alarm.models import AlarmHistory
from OperationManagementSystem.apps.system.models import RDS, RDSUsageRecord
import datetime
import time


def get_alarm_history_list():
    start_time = str(datetime.datetime.now() - datetime.timedelta(days=7))[:19]
    end_time = str(datetime.datetime.now())[:19]
    result = acs_alarm_history.acs_alarm_history(starttime=start_time, endtime=end_time)
    for h in result:
        if h['Status'] == 0:
            name = h['Name']
            namespace = h['Namespace']
            alarm_time = h['AlarmTime']
            alarm_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(alarm_time / 1000))
            value = h['Value']
            instance_name = h['InstanceName']
            metric_name = h['MetricName']
            dimension = h['Dimension']
            if AlarmHistory.objects.filter(alarm_time=alarm_time).count() == 0:
                alarm = AlarmHistory(name=name, namespace=namespace, alarm_time=alarm_time, value=value,
                                     instance_name=instance_name, metric_name=metric_name, dimension=dimension)
                alarm.save()


def get_rds_info():
    result = acs_rds_info.query_rds_list(RegionId="cn-hangzhou")
    if RDS.objects.filter(instance_id=result['DBInstanceId']).count() == 0:
        rds = RDS(instance_id=result['DBInstanceId'], network_type=result['InstanceNetworkType'],
                  engine=result['Engine'], engine_version=result['EngineVersion'], status=result['DBInstanceStatus'],
                  expire_time=result['ExpireTime'].replace("Z", "").replace("T", " "))
        rds.save()


def get_rds_monitor():
    # 记录最新RDS资源数据
    for rds in RDS.objects.all():
        rds_instance_id = rds.instance_id.encode('utf8')
        cpu_usage = acs_rds_monitor.query_rds_monitor(instanceId=rds_instance_id, metric="CpuUsage")
        io_usage = acs_rds_monitor.query_rds_monitor(instanceId=rds_instance_id, metric="IOPSUsage")
        disk_usage = acs_rds_monitor.query_rds_monitor(instanceId=rds_instance_id, metric="DiskUsage")
        print cpu_usage, io_usage, disk_usage
        rds_usage_record = RDSUsageRecord(cpu_usage=cpu_usage, io_usage=io_usage, disk_usage=disk_usage,
                                          rds_id=rds.id)
        rds_usage_record.save()
    # 删除超过14天数据
    now = datetime.datetime.now()
    pass_time = now - datetime.timedelta(days=14)
    rds_usage_record = RDSUsageRecord.objects.filter(add_time__lt=pass_time)
    rds_usage_record.delete()
