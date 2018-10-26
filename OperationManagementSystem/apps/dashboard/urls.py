# -*- coding: utf-8 -*-

from django.conf.urls import url
from apscheduler.schedulers.background import BackgroundScheduler
from . import views
from . import cron

app_name = 'dashboard'

urlpatterns = [
    # alarm
    url(r'^alarm_charts/$', views.alarm_charts, name='alarm_charts'),
    url(r'^index_alarm_product_type_pie/$', views.index_alarm_product_type_pie, name='index_alarm_product_type_pie'),
    url(r'^index_alarm_metric_type_pie/$', views.index_alarm_metric_type_pie, name='index_alarm_metric_type_pie'),
    url(r'^index_alarm_instance_pie/$', views.index_alarm_instance_pie, name='index_alarm_instance_pie'),
    url(r'^index_alarm_line/$', views.index_alarm_line, name='index_alarm_line'),
    # rds
    url(r'^rds_charts/$', views.rds_charts, name='rds_charts'),
    url(r'^index_rds_cpu_pie/$', views.index_rds_cpu_pie, name='index_rds_cpu_pie'),
    url(r'^index_rds_io_pie/$', views.index_rds_io_pie, name='index_rds_io_pie'),
    url(r'^index_rds_disk_pie/$', views.index_rds_disk_pie, name='index_rds_disk_pie'),
    url(r'^index_rds_line/$', views.index_rds_line, name='index_rds_line'),
]


scheduler = BackgroundScheduler()


@scheduler.scheduled_job("interval", seconds=500, id="get_alarm_history")
def get_alarm_history():
    cron.get_alarm_history_list()
    print ("get_alarm_history")


scheduler.start()
