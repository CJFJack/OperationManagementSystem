# -*- coding: utf-8 -*-

from django.conf.urls import url
from apscheduler.schedulers.background import BackgroundScheduler
from django.views.generic import TemplateView
from . import cron, views

app_name = 'alarm'

urlpatterns = [
    url(r'^charts/$', TemplateView.as_view(template_name="dashboard/alarm.html"), name='charts'),
    url(r'^index_alarm_product_type_pie/$', views.index_alarm_product_type_pie, name='index_alarm_product_type_pie'),
    url(r'^index_alarm_metric_type_pie/$', views.index_alarm_metric_type_pie, name='index_alarm_metric_type_pie'),
    url(r'^index_alarm_instance_pie/$', views.index_alarm_instance_pie, name='index_alarm_instance_pie'),
    url(r'^index_alarm_line/$', views.index_alarm_line, name='index_alarm_line'),
]

scheduler = BackgroundScheduler()


@scheduler.scheduled_job("interval", seconds=500, id="get_alarm_history")
def get_alarm_history():
    cron.get_alarm_history_list()
    print ("get_alarm_history")


scheduler.start()
