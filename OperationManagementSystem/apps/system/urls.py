# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'system'


urlpatterns = [
    url(r'^ecs/$', views.ECSListView.as_view(), name='ecs_manage'),
    url(r'^sync_all_ecs_from_acs/$', views.sync_all_ecs_from_acs, name='sync_all_ecs_from_acs'),
    url(r'^update_all_ecs_info/$', views.update_all_ecs_info, name='update_all_ecs_info'),
    url(r'^ecs_table_refresh/$', views.ecs_table_refresh, name='ecs_table_refresh'),
    url(r'^update_all_ecs_monitor/$', views.update_all_ecs_monitor, name='update_all_ecs_monitor')
]