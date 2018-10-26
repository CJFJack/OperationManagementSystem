# -*- coding: utf-8 -*-

from acs_api import acs_alarm_history

from OperationManagementSystem.apps.alarm.models import AlarmHistory
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
